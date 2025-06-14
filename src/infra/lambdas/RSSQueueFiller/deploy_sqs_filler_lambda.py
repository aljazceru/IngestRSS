import os
import zipfile
import logging
import boto3
from dotenv import load_dotenv
from src.infra.deploy_infrastructure import deploy_cloudformation

# Load environment variables
load_dotenv(override=True)

# Set up logging

logging.basicConfig(level=os.getenv('LOG_LEVEL'))


# Set up S3 client
s3 = boto3.client('s3')

def zip_lambda_code():
    lambda_dir = 'src/infra/lambdas/RSSQueueFiller/lambda'
    zip_path = 'tmp/lambda_function.zip'
    
    os.makedirs(zip_path.split("/")[0], exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(lambda_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, lambda_dir)
                zipf.write(file_path, arcname)
    
    return zip_path

def upload_to_s3(file_path):
    s3_key = os.getenv('QUEUE_FILLER_LAMBDA_S3_KEY')
    bucket_name = os.getenv('S3_LAMBDA_ZIPPED_BUCKET_NAME')
    s3.upload_file(file_path, bucket_name, s3_key)
    return f's3://{bucket_name}/{s3_key}'

def deploy_sqs_filler():
    zip_file = zip_lambda_code()
    upload_to_s3(zip_file)
    
    # Deploy CloudFormation
    deploy_cloudformation('rss_lambda_stack.yaml', 'LambdaSQSFiller',
                          parameters=[
                            {
                                'ParameterKey': 'QueueFillerLambdaName',
                                'ParameterValue': os.getenv('QUEUE_FILLER_LAMBDA_NAME')
                            },
                            {
                                'ParameterKey': 'RedisUrl',
                                'ParameterValue': os.getenv('REDIS_URL')
                            },
                            {
                                'ParameterKey': 'RedisQueueName',
                                'ParameterValue': os.getenv('REDIS_QUEUE_NAME')
                            },
                            {
                                'ParameterKey': 'LambdaCodeS3Bucket',
                                'ParameterValue': os.getenv('S3_LAMBDA_ZIPPED_BUCKET_NAME')
                            },
                            {
                                'ParameterKey': 'LambdaCodeS3Key',
                                'ParameterValue': os.getenv('QUEUE_FILLER_LAMBDA_S3_KEY')
                            },
                            { 
                                'ParameterKey': 'LambdaRuntime',
                                'ParameterValue': os.getenv('LAMBDA_RUNTIME')
                            },
                            {
                                'ParameterKey': 'LambdaTimeout',
                                'ParameterValue': os.getenv('LAMBDA_TIMEOUT')
                            }
                          ])
    
    # Clean up local zip file
    os.remove(zip_file)

if __name__ == "__main__":
    deploy_sqs_filler()