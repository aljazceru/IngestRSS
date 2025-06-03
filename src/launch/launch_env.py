import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm
from utils import animate_text, get_env_value, display_summary, save_env_file, emojis, get_aws_regions

console = Console()

def check_aws_credentials():
    try: 
        os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY')
        
        return True
    except KeyError:
        return False

def check_aws_region():
    try:
        os.environ.get('AWS_REGION')
        return True
    except KeyError:
        return False
    

def main():
    animate_text("Welcome to the Ingest RSS Environment Setup!", emojis)
    console.print(Panel(Text("Welcome to the Ingest RSS Environment Setup! 🌴🌻🦍", style="bold green")))
    
    console.print(Panel(Text("Let's configure your environment variables", style="bold yellow")))
    
    env_vars = {}
    
    # Determine if we're in advanced mode
    advanced_mode = not Confirm.ask("Do you want to use basic mode? \n( We recommend basic for your first time ) ")

    # MongoDB and Redis Configuration
    env_vars["MONGODB_URL"] = get_env_value("MONGODB_URL", "Enter MongoDB URL:", options=["mongodb://localhost:27017"], advanced=advanced_mode)
    env_vars["MONGODB_ARTICLES_DB_NAME"] = get_env_value("MONGODB_ARTICLES_DB_NAME", "Enter MongoDB Articles DB Name:", options=["articles_db"], advanced=advanced_mode)
    env_vars["MONGODB_ARTICLES_COLLECTION_NAME"] = get_env_value("MONGODB_ARTICLES_COLLECTION_NAME", "Enter MongoDB Articles Collection Name:", options=["articles"], advanced=advanced_mode)
    env_vars["MONGODB_FEEDS_DB_NAME"] = get_env_value("MONGODB_FEEDS_DB_NAME", "Enter MongoDB Feeds DB Name:", options=["feeds_db"], advanced=advanced_mode)
    env_vars["MONGODB_FEEDS_COLLECTION_NAME"] = get_env_value("MONGODB_FEEDS_COLLECTION_NAME", "Enter MongoDB Feeds Collection Name:", options=["rss_feeds"], advanced=advanced_mode)
    env_vars["REDIS_URL"] = get_env_value("REDIS_URL", "Enter Redis URL:", options=["redis://localhost:6379"], advanced=advanced_mode)
    env_vars["REDIS_QUEUE_NAME"] = get_env_value("REDIS_QUEUE_NAME", "Enter Redis Queue Name:", options=["rss-feed-queue"], advanced=advanced_mode)
    
    # Logging Configuration
    env_vars["LOG_LEVEL"] = get_env_value("LOG_LEVEL", "Enter Log Level:", options=["DEBUG", "INFO", "WARNING", "ERROR"], advanced=advanced_mode)
    
    # Other Application Settings
    env_vars["APP_NAME"] = get_env_value("APP_NAME", "Enter Application Name:", options=["RSS Feed Processor", "Custom RSS Processor"], advanced=advanced_mode)
    env_vars["VERSION"] = get_env_value("VERSION", "Enter Version:", options=["1.0.0", "1.1.0", "2.0.0"], advanced=advanced_mode)
    env_vars["TEST"] = get_env_value("TEST", "Enter Test Value:", options=["0", "1"], advanced=advanced_mode)
    
    # Storage Strategy
    env_vars["STORAGE_STRATEGY"] = "mongodb"

    # Qdrant Configuration (only if qdrant is selected)
    if env_vars["STORAGE_STRATEGY"] == "qdrant":
        env_vars["QDRANT_URL"] = get_env_value("QDRANT_URL", "Enter Qdrant URL:", options=["http://localhost:6333"], advanced=advanced_mode)
        env_vars["QDRANT_COLLECTION_NAME"] = get_env_value("QDRANT_COLLECTION_NAME", "Enter Qdrant Collection Name:", options=["open-rss-articles"], advanced=advanced_mode)

    # Display summary
    display_summary(env_vars)
    
    # Save to .env file
    save_env_file(env_vars)
    
    animate_text("Environment setup complete! Happy RSS ingesting! 🎉", emojis)

if __name__ == "__main__":
    main()