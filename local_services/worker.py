import os
import time
import logging

from src.infra.lambdas.RSSFeedProcessorLambda.src.lambda_function import lambda_handler

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

SLEEP_SECONDS = int(os.getenv("WORKER_SLEEP_SECONDS", "5"))

def main():
    logger.info("Starting worker loop")
    while True:
        try:
            lambda_handler({}, None)
        except Exception as exc:
            logger.exception("Worker iteration failed: %s", exc)
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
