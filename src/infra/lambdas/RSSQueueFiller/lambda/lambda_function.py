import json
import os
import logging
from datetime import datetime
import redis

logger = logging.getLogger()
logger.setLevel("INFO")

REDIS_URL = os.environ["REDIS_URL"]
REDIS_QUEUE_NAME = os.environ.get("REDIS_QUEUE_NAME", "rss-feed-queue")
RSS_FEEDS_FILE = os.environ.get("RSS_FEEDS_FILE", "rss_feeds.json")

redis_client = redis.Redis.from_url(REDIS_URL)

def handler(event, context):
    messages_sent = 0
    try:
        with open(RSS_FEEDS_FILE, "r") as f:
            feeds = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load RSS feed file: {e}")
        return {"statusCode": 500, "body": "Failed to load feeds"}

    for feed in feeds:
        message = {"u": feed.get("u"), "dt": feed.get("dt")}
        try:
            redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(message))
            messages_sent += 1
        except Exception as e:
            logger.error(f"Error pushing message to Redis: {e}")

    logger.info(
        f"Sent {messages_sent} messages to Redis at {datetime.now().isoformat()}"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(f"Sent {messages_sent} RSS URLs to Redis"),
    }
