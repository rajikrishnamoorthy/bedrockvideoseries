import boto3
import json

# Initialize the Bedrock client
client = boto3.client('bedrock-runtime')

# Specify the model you want to use for embeddings
model_id = "amazon.titan-embed-text-v1"

# The text you want to generate embeddings for
input_text = "Morning"

# Convert the input to JSON with the correct key "inputText" and then encode as bytes
payload = json.dumps({
    "inputText": input_text  # Use "inputText" as shown in the API request from the screenshot
}).encode('utf-8')

# Define the parameters for the API request
response = client.invoke_model(
    modelId=model_id,
    body=payload,  # body must be bytes
    contentType="application/json",
    accept="*/*"
)

# Read the response and decode it from the stream
response_body = response['body'].read()  # Read the StreamingBody content
response_decoded = response_body.decode('utf-8')  # Decode the bytes to a string

# Convert the string response to JSON (the embeddings data should be here)
embedding_output = json.loads(response_decoded)

# Print the embeddings output
print(json.dumps(embedding_output, indent=4))  
