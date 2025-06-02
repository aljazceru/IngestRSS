import os
import sys
import time
import logging

# Ensure project root is in the Python path so imports work when executed
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.infra.lambdas.RSSFeedProcessorLambda.src.lambda_function import lambda_handler

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main() -> None:
    """Continuously run the existing Lambda handler as a local worker."""
    logger.info("Starting local RSS worker")
    while True:
        try:
            lambda_handler({}, None)
        except Exception as exc:
            logger.error("Worker iteration failed", exc_info=exc)
        time.sleep(1)


if __name__ == "__main__":
    main()
