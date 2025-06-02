import json
import os
import boto3
from decimal import Decimal
from datetime import datetime
import logging
from pymongo import MongoClient

logger = logging.getLogger()
logger.setLevel("INFO")

sqs = boto3.client('sqs')

SQS_QUEUE_URL = os.environ['SQS_QUEUE_URL']
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
            logger.debug("message", message)
            try:
                sqs.send_message(
                    QueueUrl=SQS_QUEUE_URL,
                    MessageBody=json.dumps(message, cls=DecimalEncoder)
                )
                messages_sent += 1
            except Exception as e:
                logger.error(f"Error sending message to SQS: {str(e)}")

    logger.info(f"Sent {messages_sent} messages to SQS at {datetime.now().isoformat()}")

    return {
        'statusCode': 200,
        'body': json.dumps(f'Sent {messages_sent} RSS URLs to SQS')
    }