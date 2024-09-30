import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Vulnerability 1: No validation of input parameters
    bucket_name = event['bucket']
    file_name = event['file']
    
    # Vulnerability 2: Hardcoded credentials (Avoid storing credentials in the code)
    access_key = 'hardcoded-access-key'
    secret_key = 'hardcoded-secret-key'
    
    # Vulnerability 3: Lack of error handling
    s3.put_object(Bucket=bucket_name, Key=file_name, Body="Sample Data")
    
    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully')
    }


