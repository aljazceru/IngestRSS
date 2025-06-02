import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_rss_feeds(rss_feeds, file_path):
    """Persist RSS feed definitions to a local JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(rss_feeds, f)
        logger.info(f"Saved {len(rss_feeds)} feeds to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save feeds: {e}")


if __name__ == "__main__":
    rss_feed_path = "rss_feeds.json"
    with open(rss_feed_path) as f:
        rss_feeds = json.load(f)
    logger.info(f"Loaded RSS feeds: {rss_feeds}")
    upload_rss_feeds(rss_feeds, rss_feed_path)
