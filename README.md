# rediskmeans [![Build Status](https://travis-ci.org/saromanov/rediskmeans.svg?branch=master)](https://travis-ci.org/saromanov/rediskmeans)
Get list of keys from redis, group them and get(or put in redis) result clusters.

Experimental


## Usage
```python
rkm = rediskmeans.RedisKMeans()
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
