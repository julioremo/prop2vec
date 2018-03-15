import pycurl

INFOBOXPROPS_URL = 'http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_en.ttl.bz2'
MBOBJECTS_URL = 'http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2'
LABELS_URL = 'http://downloads.dbpedia.org/2016-10/core-i18n/en/labels_en.ttl.bz2'

PRETRAINEDVECTORS_URL = 'https://googledrive.com/host/0B7XkCwpI5KDYeFdmcVltWkhtbmM'
PRETRAINEDVECTORS_FILE = 'freebase-vectors-skipgram1000-en.bin.gz'


def download_tofile(url, filename=None):
    if filename is None:
        filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.VERBOSE, True)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

if __name__ == "__main__":
    download_tofile(INFOBOXPROPS_URL)
    download_tofile(MBOBJECTS_URL)
    download_tofile(LABELS_URL)
    download_tofile(PRETRAINEDVECTORS_URL, PRETRAINEDVECTORS_FILE)
    print('done')
