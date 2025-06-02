import os

# Redis Configuration
REDIS_URL = os.environ["REDIS_URL"]
REDIS_QUEUE_NAME = os.environ.get("REDIS_QUEUE_NAME", "rss-feed-queue")

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# RSS Feed Processing Configuration
MAX_ARTICLES_PER_FEED = int(os.environ.get("MAX_ARTICLES_PER_FEED", "10"))
FEED_PROCESSING_TIMEOUT = int(os.environ.get("FEED_PROCESSING_TIMEOUT", "90"))

# Article Extraction Configuration
ARTICLE_EXTRACTION_TIMEOUT = int(os.environ.get("ARTICLE_EXTRACTION_TIMEOUT", "30"))
