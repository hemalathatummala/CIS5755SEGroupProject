import redis

#copy primary end point url of redis elasticache
store = redis.from_url('redis://sessionstore.bxgo7b.0001.use1.cache.amazonaws.com:6379')

store.ping()