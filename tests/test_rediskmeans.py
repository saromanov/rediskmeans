from rediskmeans import RedisKMeans
import unittest


NAMES = ["n1","n2","n3","n4","n5","n6","n7","n8","n9","n10","n11"]
class TestClusteringWithTFIDF(unittest.TestCase):
    def test_basic(self):
        rkm = RedisKMeans()
        rkm.put("one1", "music this great")
        rkm.put("one2", "Kate told me about herself")
        rkm.put("one3", "Listen music")
        rkm.put("one4", "He told this")
        result = rkm.apply(["one1", "two2", "one3", "one4"], tfidf=True, n_clusters=2)
        self.assertEqual(len(result),4)

    def test_with_numbers(self):
        rkm = RedisKMeans()
        rkm.put("n1", [0.8,0.7,0.6,0.2,0.1])
        rkm.put("n2", [0.2,0.5,0.5,0.4,0.7])
        rkm.put("n3", [0.3,0.3,0.5,0.2,0.8])
        rkm.put("n4", [0.4,0.1,0.2,0.1,0.2])
        rkm.put("n5", [0.8,0.4,0.9,0.0,0.4])
        rkm.put("n6", [0.1,0.0,0.3,0.9,0.3])
        rkm.put("n7", [0.2,0.2,0.2,0.0,0.6])
        rkm.put("n8", [0.3,0.7,0.1,0.8,0.5])
        rkm.put("n9", [0.0,0.7,0.7,0.5,0.4])
        rkm.put("n10", [0.7,0.4,0.3,0.3,0.1])
        rkm.put("n11", [0.9,0.3,0.1,0.1,0.8])
        result = rkm.apply(NAMES, n_clusters=3)
        self.assertEqual(len(result),11)
        self.assertEqual(set(result),3)
