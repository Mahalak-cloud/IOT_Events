import os
from redis import Redis
from rq import Connection, Queue
from custom_worker import WindowsWorker

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = WindowsWorker(map(Queue, listen), timeout=30)  # Set timeout as needed
        worker.work()
