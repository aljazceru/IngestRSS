import json
import os
import logging
import time

from pymongo import MongoClient
from datetime import datetime
import redis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Local deployment - Redis only
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'rss-feed-queue')

MONGODB_URL = os.environ['MONGODB_URL']
MONGODB_FEEDS_DB_NAME = os.environ.get('MONGODB_FEEDS_DB_NAME', 'feeds_db')
MONGODB_FEEDS_COLLECTION_NAME = os.environ.get('MONGODB_FEEDS_COLLECTION_NAME', 'rss_feeds')

mongo_client = MongoClient(MONGODB_URL)
feeds_collection = mongo_client[MONGODB_FEEDS_DB_NAME][MONGODB_FEEDS_COLLECTION_NAME]

# Calculate timestamp for 48 hours ago
dt_48h_ago = int(time.time()) - 48 * 3600

# Update all feeds
feeds_collection.update_many({}, {"$set": {"dt": dt_48h_ago}})

def scheduler_main():
    messages_sent = 0

    # Iterate over all feeds in MongoDB
    for item in feeds_collection.find({}):
        rss_url = item.get('url')
        rss_dt = item.get('dt')

        logger.debug(f"Processing RSS feed: {rss_url}")
        logger.debug(f"Last published date: {rss_dt}")
        
        if rss_url:
            message = {
                'u': rss_url,
                'dt': rss_dt
            }
            logger.debug(f"Message: {message}")
            
            try:
                # Send to Redis for local deployment
                redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(message))
                messages_sent += 1
            except Exception as e:
                logger.error(f"Error sending message to queue: {str(e)}")

    logger.info(f"Sent {messages_sent} messages to queue at {datetime.now().isoformat()}")

    return