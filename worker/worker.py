import redis
import time
import os
import signal

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")
PROCESSING_DELAY = int(os.getenv("PROCESSING_DELAY", 2))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD or None,
    decode_responses=False
)

running = True

def handle_shutdown(signum, frame):
    global running
    print("Shutdown signal received. Stopping worker gracefully...")
    running = False

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(PROCESSING_DELAY)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")

while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode())
    except redis.RedisError as err:
        print(f"Redis error: {err}")
        time.sleep(2)
    except Exception as err:
        print(f"Unexpected error: {err}")
        time.sleep(2)
        