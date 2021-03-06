import redis
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np


class RedisKMeans:

    def __init__(self, *args, **kwargs):
        """
        Initialization of RedisKMeans
        Args:
            addr - host for redis server
            port - port for redis server
        Example:
            RedisKMeans(addr='localhost', port=6739)
        """
        self.addr = kwargs.get('host')
        self.port = kwargs.get('port')
        if self.addr is None or self.port is None:
            self.client = redis.Redis()
        else:
            self.client = redis.Redis(host=self.addr, port=self.port)

    def put(self, key, values, path=None):
        ''' put values to redis by key
            Args:
                key - can be only as a string
                values - can be:

                array of float/int
                [0.1,0.2,0.3]
                In this case, values store in the list

                string
                In this case, strings store as string type in redis

                optional arguments:
                    path - provides path to file. Data from file using as value

            Examples:
                >>> put("abc", [0.4,0.5,0.6,0.7])
                >>> put("cba", "This is simple")
                >>> put("def", None, path="/home/username/file")
        '''
        if path is not None:
            f = open(path, 'r')
            if not os.path.exists:
                raise Exception("File is not found")
            values = f.read()
            f.close()
        if type(values) == str:
            if not self.client.exists(key):
                self.client.append(key, values)
            return
        if self._checker(values, float) or self._checker(values, int):
            self.client.lpush(key, self._preprocess(values))
            return
        raise TypeError("Not recoginzed type of values")

    def putPrefix(self, key, values, path=None):
        '''
           put data to redis with prefix "rk_"
           It helps to clustering data without naming of key
        '''
        key = 'rk_{0}'.format(key)
        self.put(key, values, path=path)

    def _checker(self, values, typ):
        '''Checker before store in redis need to recogize
           type of objects in values
        '''
        return all([isinstance(value, typ) for value in values])

    def _preprocess(self, values):
        ''' Preprocessing before put in redis.
            Now in the case of non string values
        '''
        return ' '.join(map(str, values))

    def _postprocessing(self, values):
        if len(values) == 0:
            return
        values = values[0]
        splitter = values.split()
        return list(map(float, splitter))

    def _getValues(self, keyvalues, postprocess=True):
        for (key, value) in keyvalues.items():
            if postprocess is False:
                yield value
            else:
                postvalue = self._postprocessing(value)
                if postvalue is not None:
                    yield postvalue

    def get(self, keys):
        return {key: self.client.lrange(key, 0, -1) for key in keys}

    def _get_strings(self, keys):
        return [self.client.get(key) for key in keys if self.client.exists(key)]

    def _store_as_clusters(self, clusters):
        ''' After fit in KMeans set values by clusters '''
        for clustername in clusters.keys():
            self.put(clustername, clusters[clustername])

    def apply(self, keys, n_clusters=2, KMeansmodel=None,
              title_clusters=[], tfidf=False, path='', state=None):
        """ this function provides getting data from redis
            and transform to clusters.

            Args:
                keys - Getting data by keys

                n_clusters - Number of clusters to transform data

                KMeansmodel - model for clusterization. Generally, can be any cluster
                model from sklearn

                title_clusters - After clustering, all clusters marked as numbers.
                If title_clusters is not empty, this clusters will be replace to names
                from title_clusters

                tfidf - Apply tfidf before clustering

                path - to file with keys

                state - apply target state for clustering. By default is random state
        """

        if path != '':
            f = open(path, 'r')
            keys = [key.split('\n')[0] for key in f.readlines()]
            f.close()

        if not isinstance(keys, list) or len(keys) == 0:
            return
        if not self._checker(keys, str):
            return
        kmeans = KMeans(n_clusters=n_clusters, n_jobs=-1)
        if KMeansmodel is not None:
            kmeans = KMeansmodel
        if state is not None:
            kmeans = KMeans(n_clusters=n_clusters, n_jobs=-1)
        if not tfidf:
            keyvalues = self.get(keys)
            values = list(self._getValues(keyvalues, postprocess=not tfidf))
            values = np.array(values)/np.max(values)
        else:
            keyvalues = self._get_strings(keys)
            values = tfidf_transform(keyvalues)
        if len(keys) != len(values):
            raise Exception("Number of keys is not equal to number of values")

        result = kmeans.fit_predict(values)
        if title_clusters != [] and len(title_clusters) != n_clusters:
            raise Exception(
                "Names of clusters can't be greater than number of clusters")
        return result if title_clusters == [] else [title_clusters[i] for i in result]

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

    def apply_and_store(self, keys, n_clusters=2,
                        KMeansmodel=None, title_clusters=[], tfidf=False):
        result = self.apply(
            keys, n_clusters=n_clusters,
            KMeansmodel=KMeansmodel, title_clusters=title_clusters, tfidf=tfidf)
        clusternames = ['cluster_{0}'.format(num) for num in result]\
            if title_clusters is None\
            else title_clusters
        datavalues = self._associate(clusternames,
                                     list(self._getValues(self.get(keys))))
        self._store_as_clusters(datavalues)


def tfidf_transform(X):
    vectorizer = TfidfVectorizer(min_df=1, max_df=0.9,
                                 stop_words='english', decode_error='ignore')
    return vectorizer.fit_transform(X)
