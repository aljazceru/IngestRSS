import json
import os
from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_rss_feeds(rss_feeds, mongo_url, db_name, collection_name):
    client = MongoClient(mongo_url)
    collection = client[db_name][collection_name]

    logger.info(f"Uploading RSS feeds to MongoDB collection: {collection_name}")

    new_items = 0
    existing_items = 0

    for feed in rss_feeds:
        url = feed.get('u')
        dt = int(feed.get('dt', 0))
        result = collection.update_one(
            {'url': url},
            {'$setOnInsert': {'url': url, 'dt': dt}},
            upsert=True
        )
        if result.upserted_id:
            new_items += 1
        else:
            existing_items += 1

    logger.info(
        f"Upload complete. {new_items} new items inserted. {existing_items} items already existed."
    )

if __name__ == "__main__":
    mongo_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('MONGODB_DB_NAME', 'ingestrss')
    collection_name = os.getenv('MONGODB_COLLECTION_NAME', 'rss_feeds')
    with open('rss_feeds.json') as f:
        rss_feeds = json.load(f)
    logger.info(f"Loaded RSS feeds: {rss_feeds}")
    upload_rss_feeds(rss_feeds, mongo_url, db_name, collection_name)
