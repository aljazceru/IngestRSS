import json
import os
import logging
import boto3
from decimal import Decimal
from pymongo import MongoClient
from datetime import datetime
import redis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# For AWS deployment - SQS
try:
    sqs = boto3.client('sqs')
    SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL', '')
    AWS_DEPLOYMENT = bool(SQS_QUEUE_URL)
except Exception:
    AWS_DEPLOYMENT = False

# For local deployment - Redis
if not AWS_DEPLOYMENT:
    redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
    REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'rss-feed-queue')

MONGODB_URL = os.environ['MONGODB_URL']
MONGODB_DB_NAME = os.environ['MONGODB_DB_NAME']
MONGODB_COLLECTION_NAME = os.environ.get('MONGODB_COLLECTION_NAME', 'rss_feeds')

mongo_client = MongoClient(MONGODB_URL)
feeds_collection = mongo_client[MONGODB_DB_NAME][MONGODB_COLLECTION_NAME]

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
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
                if AWS_DEPLOYMENT:
                    # Send to SQS for AWS deployment
                    sqs.send_message(
                        QueueUrl=SQS_QUEUE_URL,
                        MessageBody=json.dumps(message, cls=DecimalEncoder)
                    )
                else:
                    # Send to Redis for local deployment
                    redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(message, cls=DecimalEncoder))
                messages_sent += 1
            except Exception as e:
                logger.error(f"Error sending message to queue: {str(e)}")

    logger.info(f"Sent {messages_sent} messages to queue at {datetime.now().isoformat()}")

    return {
        "statusCode": 200,
        "body": json.dumps(f"Sent {messages_sent} RSS URLs to queue"),
    }