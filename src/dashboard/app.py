from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pymongo import MongoClient
import os
import json

app = FastAPI()

# Serve static files (HTML/JS)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# MongoDB setup
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_FEEDS_DB_NAME = os.environ.get("MONGODB_FEEDS_DB_NAME", "feeds_db")
MONGODB_FEEDS_COLLECTION_NAME = os.environ.get("MONGODB_FEEDS_COLLECTION_NAME", "rss_feeds")
mongo_client = MongoClient(MONGODB_URL)
feeds_collection = mongo_client[MONGODB_FEEDS_DB_NAME][MONGODB_FEEDS_COLLECTION_NAME]

@app.get("/")
def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.get("/api/feeds")
def get_feeds():
    feeds = list(feeds_collection.find({}, {"_id": 0}))
    return JSONResponse(content=feeds)

@app.post("/api/feeds")
async def add_feed(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(content={"error": "Missing URL"}, status_code=400)
    feeds_collection.update_one({"url": url}, {"$setOnInsert": {"url": url, "dt": 0}}, upsert=True)
    return JSONResponse(content={"status": "ok"})

@app.delete("/api/feeds")
async def delete_feed(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(content={"error": "Missing URL"}, status_code=400)
    feeds_collection.delete_one({"url": url})
    return JSONResponse(content={"status": "ok"})

# Add similar endpoints for schedules and job status as needed
