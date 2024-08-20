import redis
import json


# redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
redis_client = redis.Redis(
  host='redis-12225.c15.us-east-1-4.ec2.redns.redis-cloud.com',
  port=12225,
  password='xadCJa5TsjjVgGzxHPzP0mRY9LUhJcPT')

def save_recipe_in_cache(recipe_id, recipe_data):
    return redis_client.set(recipe_id, json.dumps(recipe_data))

def get_recipe_from_cache():
  recipe_json = redis_client.get('current_recipe')

  if not recipe_json:
    return None
  return json.loads(recipe_json)
