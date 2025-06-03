import os
import time
import logging

from src.feed_processing.worker_main import worker_main

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

SLEEP_SECONDS = int(os.getenv("WORKER_SLEEP_SECONDS", "5"))

def main():
    logger.info("Starting worker loop")
    while True:
        try:
            worker_main()
        except Exception as exc:
            logger.exception("Worker iteration failed: %s", exc)
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
