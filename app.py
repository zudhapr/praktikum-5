from flask import Flask, jsonify
from redis import Redis
import os

app = Flask(__name__)
cache = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

@app.get("/")
def index():
    visits = cache.incr("visits")
    return jsonify(service="simple-lms", visits=visits)

@app.get("/health")
def health():
    return {"status": "ok"}

app.run(host="0.0.0.0", port=5000)
