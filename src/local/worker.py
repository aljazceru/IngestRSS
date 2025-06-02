import os
import sys
import time
import logging

# Add the project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.infra.lambdas.RSSFeedProcessorLambda.src.lambda_function import lambda_handler

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

SLEEP_SECONDS = int(os.getenv("WORKER_SLEEP_SECONDS", "5"))

def main():
    logger.info("Starting worker loop")
    while True:
        try:
            result = lambda_handler({}, None)
            if result.get('statusCode') == 200:
                logger.debug("Worker iteration completed successfully")
            else:
                logger.warning(f"Worker iteration returned non-200 status: {result}")
        except Exception as exc:
            logger.exception("Worker iteration failed: %s", exc)
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()