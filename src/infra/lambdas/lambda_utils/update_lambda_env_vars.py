import boto3
import os
from src.utils.retry_logic import retry_with_backoff

# Set variables
LAMBDA_NAME = "RSSFeedProcessor"

@retry_with_backoff()
def update_env_vars(function_name):
    lambda_client = boto3.client('lambda')

    env_vars = {
        
        # Lambda Configuration
        'LAMBDA_FUNCTION_NAME': os.environ.get('LAMBDA_FUNCTION_NAME'),
        'STACK_BASE': os.environ.get('STACK_BASE'),
        'LAMBDA_EXECUTION_ROLE_NAME': os.environ.get('LAMBDA_EXECUTION_ROLE_NAME'),
        'LAMBDA_ROLE_ARN': os.environ.get('LAMBDA_ROLE_ARN'),
        'LAMBDA_LAYER_VERSION': os.environ.get('LAMBDA_LAYER_VERSION'),
        'LAMBDA_LAYER_NAME': os.environ.get('LAMBDA_LAYER_NAME'),
        'LAMBDA_LAYER_ARN': os.environ.get('LAMBDA_LAYER_ARN'),
        'LAMBDA_RUNTIME': os.environ.get('LAMBDA_RUNTIME'),
        'LAMBDA_TIMEOUT': os.environ.get('LAMBDA_TIMEOUT', '300'),  # Reasonable default timeout
        'LAMBDA_MEMORY': os.environ.get('LAMBDA_MEMORY', '512'),  # Reasonable default memory
        
        # S3 Configuration
        'S3_BUCKET_NAME': os.environ.get('S3_BUCKET_NAME'),
        'S3_LAMBDA_ZIPPED_BUCKET_NAME': os.environ.get('S3_LAMBDA_ZIPPED_BUCKET_NAME'),
        'S3_LAYER_BUCKET_NAME': os.environ.get('S3_LAYER_BUCKET_NAME'),
        'S3_LAYER_KEY_NAME': os.environ.get('S3_LAYER_KEY_NAME'),

        # Redis Configuration
        'REDIS_URL': os.environ.get('REDIS_URL'),
        'REDIS_QUEUE_NAME': os.environ.get('REDIS_QUEUE_NAME'),
        
        # Queue Filler Lambda Configuration
        'QUEUE_FILLER_LAMBDA_NAME': os.environ.get('QUEUE_FILLER_LAMBDA_NAME'),
        'QUEUE_FILLER_LAMBDA_S3_KEY': os.environ.get('QUEUE_FILLER_LAMBDA_S3_KEY'),
        
        # Python Configuration
        'PYTHON_VERSION': os.environ.get('PYTHON_VERSION', '3.12'),  # Default Python version
        
        # Application Settings
        'APP_NAME': os.environ.get('APP_NAME', 'RSS Feed Processor'),  # Default app name is fine
        'VERSION': os.environ.get('VERSION', '1.0.0'),  # Default version is fine
        'LOG_LEVEL': os.environ.get('LOG_LEVEL', 'INFO'),  # Default to INFO logging
        
        # Storage Configuration
        'STORAGE_STRATEGY': os.environ.get('STORAGE_STRATEGY', 's3'),  # Default to s3 storage
        
        # Qdrant Configuration (only used if STORAGE_STRATEGY is 'qdrant')
        'QDRANT_URL': os.environ.get('QDRANT_URL'),
        'QDRANT_API_KEY': os.environ.get('QDRANT_API_KEY'),
        'QDRANT_COLLECTION_NAME': os.environ.get('QDRANT_COLLECTION_NAME'),
        
        # Vector Configuration
        'VECTOR_EMBEDDING_MODEL': os.environ.get('VECTOR_EMBEDDING_MODEL'),
        'VECTOR_EMBEDDING_DIM': os.environ.get('VECTOR_EMBEDDING_DIM'),
        'VECTOR_SEARCH_METRIC': os.environ.get('VECTOR_SEARCH_METRIC'),
        
        # Ollama Configuration
        'OLLAMA_HOST': os.environ.get('OLLAMA_HOST'),
        'OLLAMA_EMBEDDING_MODEL': os.environ.get('OLLAMA_EMBEDDING_MODEL'),
    }
    
    return lambda_client.update_function_configuration(
        FunctionName=LAMBDA_NAME,
        Environment={'Variables': env_vars}
    )
