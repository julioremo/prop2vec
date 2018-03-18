import bz2
import pandas as pd
from gensim.models import KeyedVectors
from itertools import islice
import re
import random.sample

INFOBOXPROPS = 'infobox_properties_en.ttl.bz2'
LABELS = 'labels_en.ttl.bz2'
PRETRAINEDVECTORS = 'freebase-vectors-skipgram1000-en.bin.gz'


def bz2_todf(filename, usecols=[0,1,2], colnames=['subject', 'property', 'object']):
    with bz2.open(filename, mode='rt') as f:
        data = pd.read_csv(f, sep=' ', header=None, skiprows=[0, -1],
                           usecols=usecols, names=colnames)
        return data


def format_DBP_toFreebase(label):
    # converts 'Hari Om (2016 film)@en' into '/en/hari_om'
    cropped = re.sub(r"\(.*\)", "", label[:-3]).strip()
    formatted = '/en/' + cropped.lower().replace(' ', '_')
    return formatted


def format_Freebase_toTitle(label):
    # converts '/en/hari_om' into 'Hari Om'
    formatted = label[4:].replace('_', ' ').title()
    return formatted


def format_results_towords(ranked_tuples):
    return [format_Freebase_toTitle(t[0]) for t in ranked_tuples]


def get_labels(p, max_labels=1000, formatted=True):
    ending = '/' + p + '>'
    objs = (row[0] for row in zip(infoboxprops['subject'], infoboxprops['property']) if ending in row[1])
    if max_labels is not 'all':
        objs = list(islice(objs, max_labels))
    labels = labelled[labelled['subject'].isin(objs)].label
    if formatted == True:
        labels = labels.apply(format_DBP_toFreebase)
    return labels


def get_vector(word):
    try:
        return word_vectors[word]
    except:
        return None


def similar_by_property(prop, n_results=10, max_labels=1000, justwords=False):
    labels = get_labels(prop, max_labels=max_labels).tolist()
    vectors = [get_vector(label) for label in labels if label in word_vectors]
    centroid = pd.Series(vectors).mean()
    results = word_vectors.similar_by_vector(centroid, n_results)
    if justwords == True:
        return format_results_towords(results)
    else:
        return results


if __name__ == "__main__":
    print('loading', INFOBOXPROPS)
    infoboxprops = bz2_todf(INFOBOXPROPS)
    print('loading', LABELS)
    labelled = bz2_todf(LABELS, usecols=[0,2], colnames=['subject', 'label'])

    allproperties = set(infoboxprops.property.drop_duplicates().apply(lambda x: x.split('/')[-1][:-1]).tolist())

    print('building Word2vec model')
    model = KeyedVectors.load_word2vec_format(PRETRAINEDVECTORS, binary=True)
    word_vectors = model.wv
    del model

    while True:
        p = input('Enter a property: ')
        if p in allproperties:
            results = similar_by_property(p)
            print('Results for '+p, *results, sep='\n')
        else:
            sample_properties = random.sample(allproperties, 3)
            print(p, 'is not a property.')
            print('You could try {1}, {2} or {3}.\n'.format(*sample_properties))
