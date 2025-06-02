import os
import sys
import json
import subprocess
import boto3
from dotenv import load_dotenv
import logging
import argparse


def check_local_env() -> None:
    """Ensure required environment variables for local mode are set."""
    required_vars = [
        "MONGODB_URL",
        "MONGODB_DB_NAME", 
        "MONGODB_COLLECTION_NAME",
        "REDIS_URL",
        "REDIS_QUEUE_NAME",
        "MINIO_ENDPOINT",
        "MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY",
        "MINIO_BUCKET",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables for local mode: {', '.join(missing)}"
        )


def start_docker_containers() -> None:
    """Start required Docker containers for local development."""
    try:
        subprocess.check_call(["docker-compose", "up", "-d"])
    except FileNotFoundError:
        # fallback to `docker compose` if docker-compose command not found
        subprocess.check_call(["docker", "compose", "up", "-d"])
    except Exception as exc:
        logging.error(f"Failed to start Docker containers: {exc}")
        raise


print("RSS Feed Processor".center(100, "-"))

parser = argparse.ArgumentParser(description="Launch IngestRSS")
parser.add_argument(
    "--local",
    action="store_true",
    help="Run locally using Docker instead of deploying to AWS",
)
args = parser.parse_args()

load_dotenv(override=True)

if args.local:
    check_local_env()
    # Upload RSS feeds to MongoDB for local deployment
    from src.feed_management.upload_rss_feeds import upload_rss_feeds
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rss_feeds_file = os.path.join(current_dir, "rss_feeds.json")
    
    if os.path.exists(rss_feeds_file):
        with open(rss_feeds_file, 'r') as f:
            rss_feeds = json.load(f)
        upload_rss_feeds(
            rss_feeds,
            os.getenv('MONGODB_URL'),
            os.getenv('MONGODB_DB_NAME'),
            os.getenv('MONGODB_COLLECTION_NAME', 'rss_feeds')
        )
        print("RSS feeds uploaded to MongoDB")
    
    start_docker_containers()
    print("Local RSS Feed Processor started successfully!")
    print("Services running:")
    print("- MongoDB: localhost:27017")
    print("- Redis: localhost:6379") 
    print("- MinIO: localhost:9000 (console: localhost:9001)")
    print("- Worker and Scheduler containers are processing feeds")
    sys.exit(0)

else:
    # Only import AWS modules for cloud deployment
    from src.utils.check_env import check_env
    from src.infra.deploy_infrastructure import deploy_infrastructure
    from src.infra.lambdas.RSSFeedProcessorLambda.deploy_rss_feed_lambda import deploy_lambda
    from src.infra.lambdas.lambda_utils.update_lambda_env_vars import update_env_vars
    from src.feed_management.upload_rss_feeds import upload_rss_feeds
    from src.infra.lambdas.RSSQueueFiller.deploy_sqs_filler_lambda import deploy_sqs_filler
    
    check_env()

# Set up logging
logging.basicConfig(level=os.getenv("LOG_LEVEL"))

lambda_client = boto3.client("lambda")

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def main(local_mode=False):
    if local_mode:
        return  # Already handled above
        
    # Deploy infrastructure
    deploy_infrastructure()
    logging.info("Finished Deploying Infrastructure")
   
    # Deploy Lambda function
    deploy_lambda()
    logging.info("Finished Deploying Lambda")

    deploy_sqs_filler()
    logging.info("Finished Deploying Queue Filler Lambda")

    # Update Lambda environment variables
    update_env_vars(os.getenv("LAMBDA_FUNCTION_NAME"))
    print("Finished Environment Variable Updates")

    # Upload RSS feeds
    rss_feeds_file = os.path.join(current_dir, "rss_feeds.json")
    if os.path.exists(rss_feeds_file):
        with open(rss_feeds_file, 'r') as f:
            rss_feeds = json.load(f)
        upload_rss_feeds(
            rss_feeds,
            os.getenv('MONGODB_URL'),
            os.getenv('MONGODB_DB_NAME'),
            os.getenv('MONGODB_COLLECTION_NAME', 'rss_feeds')
        )

    else:
        print(f"WARNING: {rss_feeds_file} not found. Skipping RSS feed upload.")

    print("RSS Feed Processor launched successfully!")

if __name__ == "__main__":
    main(args.local)