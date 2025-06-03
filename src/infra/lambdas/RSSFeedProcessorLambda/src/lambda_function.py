import json
import time
import os
import redis
from feed_processor import extract_feed
from data_storage import save_article, update_rss_feed
from utils import setup_logging
from config import REDIS_URL, REDIS_QUEUE_NAME
from exceptions import RSSProcessingError, DataStorageError
from metrics import (
    record_processed_articles,
    record_processing_time,
    record_extraction_errors,
)

logger = setup_logging()
storage_strategy = os.environ.get("STORAGE_STRATEGY")
redis_client = redis.Redis.from_url(REDIS_URL)


def lambda_handler(event, context):
    logger.info("Starting RSS feed processing")
    start_time = time.time()

    try:
        feed_data = redis_client.rpop(REDIS_QUEUE_NAME)
        if not feed_data:
            logger.info("No messages in queue")
            return {"statusCode": 200, "body": json.dumps("No feeds to process")}
        feed = json.loads(feed_data)

        result = extract_feed(feed)
        logger.info(f"Process Feed Result Dictionary: {result}")
        last_pub_dt = result["max_date"]

        if result:
            for article in result["articles"]:
                try:
                    save_article(article, storage_strategy)
                except DataStorageError as e:
                    logger.error(f"Failed to save article: {str(e)}")
                    record_extraction_errors(1)

            update_rss_feed(result["feed"], last_pub_dt)
            logger.info(f"Processed feed: {feed['u']}")
            record_processed_articles(len(result["articles"]))
        else:
            logger.warning(f"Failed to process feed: {feed['u']}")
            record_extraction_errors(1)

    except RSSProcessingError as e:
        logger.error(f"RSS Processing Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("RSS processing failed")}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("An unexpected error occurred")}

    finally:
        end_time = time.time()
        processing_time = end_time - start_time
        record_processing_time(processing_time)
        logger.info(f"Lambda execution time: {processing_time:.2f} seconds")

    return {"statusCode": 200, "body": json.dumps("RSS feed processed successfully")}
