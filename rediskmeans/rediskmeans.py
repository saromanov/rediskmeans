import redis
from sklearn.cluster import KMeans
import struct
from sklearn.feature_extraction.text import TfidfVectorizer

class RedisKMeans:

    def __init__(self, *args, **kwargs):
        self.addr = kwargs.get('host')
        self.port = kwargs.get('port')
        if self.addr == None or self.port == None:
            self.client = redis.Redis()
        else:
            self.client = redis.Redis(host=addr, port=port)

    def put(self, key, values):
        #Checker before store in redis need to recogize type of objects in values
        checker = lambda x: all([isinstance(value, x) for value in values])
        if checker(float) or checker(string) or checker(int):
            self.client.lpush(key, self._preprocess(values))
            return
        raise TypeError("Not recoginzed type of values")

    def _preprocess(self, values):
        ''' preprocessing before put in redis. Now in the case of non string values'''
        return ' '.join(map(str, values))

    def _postprocessing(self, values):
        if len(values) == 0:
            return
        values = values[0]
        splitter = values.split()
        return list(map(float, splitter))

    def _getValues(self, keyvalues):
        for (key, value) in keyvalues.items():
            postvalue = self._postprocessing(value)
            if postvalue != None:
                yield postvalue

    def get(self, keys):
        return {key: self.client.lrange(key, 0, -1) for key in keys}

    def _store_as_clusters(self, clusters):
        ''' After fit in KMeans set values by clusters '''
        for clustername in clusters.keys():
            self.put(clustername, clusters[clustername])

    def apply(self, keys, n_clusters=2, KMeansmodel=None, title_clusters=[], tfidf=False):
        if len(keys) == 0:
            return
        kmeans = KMeans(n_clusters=n_clusters)
        if KMeansmodel != None:
            kmeans = KMeansmodel
        keyvalues = self._get(keys)
        return kmeans.fit_predict(list(self._getValues(keyvalues)))

    def _associate(self, clusters, values):
        ''' Associate each cluster with list of values '''
        result = {}
        for i, name in enumerate(clusters):
            if name in result:
                result[name].append(values[i])
            else:
                print(values)
                result[name] = [values[i]]
        return result

    def apply_and_store(self, keys, n_clusters=2, KMeansmodel=None, title_clusters=None):
        result = self.apply(
            keys, n_clusters=n_clusters, KMeansmodel=KMeansmodel, title_clusters=title_clusters)
        clusternames = ['cluster_{0}'.format(
            num) for num in result] if title_clusters == None else title_clusters
        datavalues = self._associate(clusternames, list(self._getValues(self._get(keys))))
        print("Datavalues: ", datavalues)
        self._store_as_clusters(datavalues)


def tfidf_transform(X):
    vectorizer=TfidfVectorizer(min_df=1, max_df=0.9, stop_words='english', decode_error='ignore')
    return vectorizer.fit_transform(X)
