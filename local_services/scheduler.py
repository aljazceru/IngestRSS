import os
import time
import logging
import importlib

handler = importlib.import_module(
    'src.feed_management.scheduler_main'
).scheduler_main

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "240"))


def main():
    logger.info("Starting scheduler loop")
    while True:
        try:
            handler()
        except Exception as exc:
            logger.exception("Scheduler job failed: %s", exc)
        time.sleep(INTERVAL_MINUTES * 60)


if __name__ == "__main__":
    main()
