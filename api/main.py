from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD or None,
    decode_responses=False
)

@app.get("/health")
def health_check():
    try:
        r.ping()
        return {"status": "ok"}
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush(QUEUE_NAME, job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status.decode()}
