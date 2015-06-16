from rediskmeans import RedisKMeans
import unittest


class TestClusteringWithTFIDF(unittest.TestCase):
    def test_basic(self):
        rkm = RedisKMeans()
        rkm.put("one1", "music this great")
        rkm.put("one2", "Kate told me about herself")
        rkm.put("one3", "Listen music")
        rkm.put("one4", "He told this")
        result = rkm.apply(["one1", "two2", "one3", "one4"], tfidf=True, n_clusters=4)
        self.assertEqual(len(result),2)

