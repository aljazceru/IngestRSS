import schedule
import time
from src.infra.lambdas.RSSQueueFiller.lambda.lambda_function import handler


def run_queue_filler():
    """Invoke the queue filler lambda logic."""
    handler(None, None)


schedule.every(4).hours.do(run_queue_filler)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
