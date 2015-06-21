# rediskmeans
Get list of keys from redis, group them and get(or put in redis) result clusters.

Experimental


## Usage
```python
rkm = rediskmeans.RedisKMeans()
rkm.apply_and_store(["ab", "bc", "vd", "er", "ok", "po", "nj", "oi"])
rkm.get(['cluster0'])
```


## LICENSE
MIT
