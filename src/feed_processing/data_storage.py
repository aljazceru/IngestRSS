import json
import os
import logging
from pymongo import MongoClient

logger = logging.getLogger()

# Try to import vector DB components, but make them optional
try:
    from .analytics.embeddings.vector_db import get_index, upsert_vectors, vectorize
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    logger.warning("Vector DB components not available. Qdrant storage will not work.")

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_ARTICLES_DB_NAME = os.getenv("MONGODB_ARTICLES_DB_NAME", "articles_db")
MONGODB_ARTICLES_COLLECTION_NAME = os.getenv("MONGODB_ARTICLES_COLLECTION_NAME", "articles")

mongo_client = MongoClient(MONGODB_URL)
articles_collection = mongo_client[MONGODB_ARTICLES_DB_NAME][MONGODB_ARTICLES_COLLECTION_NAME]

##### Article Storage #####
def save_article(article: dict, strategy: str = None):
    # Only MongoDB is supported now
    try:
        articles_collection.insert_one(article)
        logger.info(f"Saved article {article.get('article_id', '')} to MongoDB")
    except Exception as e:
        logger.error(f"Failed to save article with error: {str(e)}. \n Article: {article} \n Article Type: {type(article)}")
        raise

###### Feed Storage ######
RSS_FEEDS_FILE = os.getenv("RSS_FEEDS_FILE", "rss_feeds.json")


def update_rss_feed(feed: dict, last_pub_dt: int):
    try:
        if not os.path.exists(RSS_FEEDS_FILE):
            return
        with open(RSS_FEEDS_FILE, "r") as f:
            feeds = json.load(f)
        for item in feeds:
            if item.get("u") == feed["u"]:
                item["dt"] = int(last_pub_dt)
        with open(RSS_FEEDS_FILE, "w") as f:
            json.dump(feeds, f)
        logger.info(f"Updated RSS feed {feed['u']} with dt: {last_pub_dt}")
    except Exception as e:
        logger.error(f"Failed to update RSS feed: {str(e)}")