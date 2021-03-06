# rediskmeans [![Build Status](https://travis-ci.org/saromanov/rediskmeans.svg?branch=master)](https://travis-ci.org/saromanov/rediskmeans)
Get list of keys from redis, group them and get(or put in redis) result clusters.

Experimental


## Usage
```python
rkm = rediskmeans.RedisKMeans()
def put():
    rkm.put("ab", [0.8, 0.4, 0.5, 0.3])
    rkm.put("bc", [0.2, 0.5, 0.1, 0.1])
    rkm.put("vd", [0.1, 0.5, 0.3, 0.4])
    rkm.put("er", [0.8, 0.4, 0.4, 0.5])
    rkm.put("ok", [0.4, 0.3, 0.8, 0.6])
    rkm.put("po", [0.2, 0.2, 0.7, 0.7])
    rkm.put("nj", [0.1, 0.9, 0.6, 0.8])
    rkm.put("oi", [0.3, 0.2, 0.3, 0.9])

rkm.apply_and_store(["ab", "bc", "vd", "er", "ok", "po", "nj", "oi"])
rkm.get(['cluster0'])
```

Read keys from file
```python
rkm = rediskmeans.RedisKMeans()
rkm.apply_and_store(path="keys")
rkm.get(['cluster0'])
```

## LICENSE
MIT
