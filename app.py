import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

app = FastAPI()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
INSTANCE_ID = os.getenv("INSTANCE_ID", "local")


def redis_client():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


class EchoIn(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok", "instance_id": INSTANCE_ID}


@app.post("/echo")
def echo(body: EchoIn):
    return {
        "message": body.message,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/increment/{key}")
def increment(key: str):
    try:
        n = redis_client().incr(key)
    except redis.exceptions.RedisError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    return {"key": key, "count": n}
