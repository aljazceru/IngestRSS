import os
import time
from dotenv import load_dotenv
from typing import List, Dict

def check_env() -> None:
    # Variables that must be set by the user
    required_user_vars = [
        "MONGODB_URL",
        "MONGODB_ARTICLES_DB_NAME",
        "MONGODB_ARTICLES_COLLECTION_NAME",
        "MONGODB_FEEDS_DB_NAME",
        "MONGODB_FEEDS_COLLECTION_NAME",
        "REDIS_URL",
        "REDIS_QUEUE_NAME"
    ]

    # Variables that are derived or have default values
    derived_vars = [
        "LOG_LEVEL",
        "APP_NAME",
        "VERSION",
        "STORAGE_STRATEGY"
    ]

    # Variables that are optional depending on the storage strategy
    optional_vars = {
        "QDRANT_URL": "qdrant",
        "QDRANT_API_KEY": "qdrant",
        "QDRANT_COLLECTION_NAME": "qdrant",
        "OLLAMA_HOST": "all",
        "OLLAMA_EMBEDDING_MODEL": "all",
        "VECTOR_EMBEDDING_MODEL": "qdrant",
        "VECTOR_EMBEDDING_DIM": "qdrant",
        "VECTOR_SEARCH_METRIC": "qdrant"
    }

    missing_vars: List[str] = []
    placeholder_vars: List[str] = []
    missing_optional_vars: List[str] = []

    # Check required user variables
    for var in required_user_vars:
        value = os.getenv(var)
        if value is None or value == "***" or value.strip() == "":
            missing_vars.append(var)

    # Check derived variables
    for var in derived_vars:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)

    # Check optional variables
    storage_strategy = os.getenv("STORAGE_STRATEGY", "").lower()
    for var, strategy in optional_vars.items():
        if strategy == "all" or strategy == storage_strategy:
            value = os.getenv(var)
            if value is None or value == "***" or value.strip() == "":
                missing_optional_vars.append(var)

    if missing_optional_vars:
        print("\nMissing or improperly set optional variables (based on your storage strategy):")
        for var in missing_optional_vars:
            print(f"- {var}")

    if missing_vars or placeholder_vars:
        print("Error: Some environment variables are not properly set.")
        
        if missing_vars:
            print("\nMissing or improperly set required variables:")
            for var in missing_vars:
                print(f"- {var}")
        
        print(f"😡👊😡Someone didn't read DIRECTIONS 😡👊😡")
        time.sleep(2)
        print("That's okay.")
        time.sleep(1.5)
        print("I don't follow directions that much either.")
        
        time.sleep(1.5)
        print("But we need to set these environment variables before running the script.")
        
        print("\n\n\n\nPlease refer to the README & template.env for additional setup instructions.\n\n\n\n")
        raise EnvironmentError("Missing or improperly set environment variables")
    else:
        print("Someone followed directions!🐝🐝🐝")
        print("All required environment variables are properly set.")

# Example usage
if __name__ == "__main__":
    load_dotenv(override=True)
    check_env()