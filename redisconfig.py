import os

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8080))
REDIS_HOST = os.getenv('REDIS_URL','localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT',6379))
