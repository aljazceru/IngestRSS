import boto3
from minio import Minio
import json
import os
import logging
from datetime import datetime
from pymongo import MongoClient

logger = logging.getLogger()

# Try to import vector DB components, but make them optional
try:
    from .analytics.embeddings.vector_db import get_index, upsert_vectors, vectorize
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    logger.warning("Vector DB components not available. Qdrant storage will not work.")

s3 = boto3.client('s3')

CONTENT_BUCKET = os.getenv("S3_BUCKET_NAME", os.getenv("CONTENT_BUCKET"))

minio_client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)
CONTENT_BUCKET = os.getenv("MINIO_BUCKET", os.getenv("S3_BUCKET_NAME", os.getenv("CONTENT_BUCKET")))
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE_NAME")
storage_strategy = os.environ.get('STORAGE_STRATEGY')

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "rss_feeds")

mongo_client = MongoClient(MONGODB_URL)
feeds_collection = mongo_client[MONGODB_DB_NAME][MONGODB_COLLECTION_NAME]

##### Article Storage #####
def save_article(article: dict, strategy: str):
    if strategy == "s3":
        s3_save_article(article)
    elif strategy == "qdrant":
        if VECTOR_DB_AVAILABLE:
            qdrant_save_article(article)
        else:
            logger.error("Qdrant storage requested but vector DB components not available")
            raise ValueError("Vector DB components not available for Qdrant storage")
    elif strategy == "both":
        if VECTOR_DB_AVAILABLE:
            qdrant_save_article(article)
        s3_save_article(article)
    else:
        raise ValueError(f"Invalid storage strategy: {strategy}")
    

def qdrant_save_article(article: dict):
    logger.info("Saving article to Qdrant")
    index = get_index()

    data = {
        "id": article["article_id"],
        "vector": vectorize(article["content"]),
        "payload": {"rss": article.get("rss"), "title": article.get("title")},
    }

    upsert_vectors(index, [data])


def s3_save_article(article:dict):
    logger.info("Saving article to MinIO")

    now = datetime.now()
    article_id = article['article_id']
    
    if not article_id:
        logger.error(f"Missing rss_id or article_id in article: {article}")
        return

    file_path = f"/tmp/{article_id}-article.json"
    file_key = f"{now.year}/{now.month}/{now.day}/{article_id}.json"
    
    # Save article to /tmp json file
    with open(file_path, "w") as f:
        json.dump(article, f)

    try:
        metadata = {
            "rss": article.get("rss", ""),
            "title": article.get("title", ""),
            "unixTime": str(article.get("unixTime", "")),
            "article_id": article.get("article_id", ""),
            "link": article.get("link", ""),
            "rss_id": article.get("rss_id", "")
        }
        minio_client.fput_object(
            CONTENT_BUCKET,
            file_key,
            file_path,
            content_type="application/json",
            metadata=metadata
        )
        logger.info(f"Saved article {article_id} to bucket {CONTENT_BUCKET}")
        
    except Exception as e:
        logger.error(f"Failed to save article with error: {str(e)}. \n Article: {article} \n Article Type: {type(article)}")


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