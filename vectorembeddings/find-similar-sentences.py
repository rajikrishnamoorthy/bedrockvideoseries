import boto3
import json
import numpy as np

# Initialize the Bedrock client for embedding
bedrock_client = boto3.client(service_name='bedrock-runtime')

# Sample flower-related facts
flower_facts = [
    'Roses are one of the most popular flowers in the world.',
    'Sunflowers can grow up to 12 feet tall.',
    'The lotus flower is sacred in many cultures.',
    'Tulips bloom in the spring and come in many colors.',
    'Daisies symbolize innocence and purity.',
]

# New sentence about flowers (for comparison)
new_flower_fact = 'Tulip is lilac in color'
flower_question = 'Which id the capital city of UAE?'

# Custom function to calculate cosine similarity using numpy
def cosine_similarity(embedding1, embedding2):
    # Convert embeddings to numpy arrays
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    
    # Calculate the dot product between the two embeddings
    dot_product = np.dot(embedding1, embedding2)
    
    # Calculate the norms of the two embeddings
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    # Return the cosine similarity
    return dot_product / (norm1 * norm2)

# Function to get text embeddings from Amazon Bedrock
def fetch_embedding(text_input: str):
    response = bedrock_client.invoke_model(
        body=json.dumps({
            "inputText": text_input,
        }), 
        modelId='amazon.titan-embed-text-v1', 
        accept='application/json', 
        contentType='application/json'
    )

    # Parse the embedding from the response
    response_content = json.loads(response.get('body').read())
    return response_content.get('embedding')

# Store flower facts along with their embeddings
flower_facts_with_embeddings = []

for flower_fact in flower_facts:
    flower_facts_with_embeddings.append({
        'text': flower_fact,
        'embedding': fetch_embedding(flower_fact)
    })

# Get the embedding for the new flower-related fact and the question
new_flower_embedding = fetch_embedding(flower_question)
new_fact_embedding = fetch_embedding(new_flower_fact)  # New addition for new_flower_fact

# Calculate cosine similarities between the new fact and the stored facts
similarity_scores = []

# Compare with flower_question
for flower_fact in flower_facts_with_embeddings:
    similarity_scores.append({
        'text': flower_fact['text'],
        'similarity': cosine_similarity(flower_fact['embedding'], new_flower_embedding),
        'comparison_type': 'flower_question'
    })

# Compare with new_flower_fact
for flower_fact in flower_facts_with_embeddings:
    similarity_scores.append({
        'text': flower_fact['text'],
        'similarity': cosine_similarity(flower_fact['embedding'], new_fact_embedding),
        'comparison_type': 'new_flower_fact'
    })

# Sort and print the results based on similarity
print(f"Similarities for comparison with '{flower_question}' and '{new_flower_fact}':")
similarity_scores.sort(key=lambda x: x['similarity'], reverse=True)

for similarity in similarity_scores:
    if similarity['comparison_type'] == 'flower_question':
        print(f"  Comparing with flower_question: '{flower_question}'")
    else:
        print(f"  Comparing with new_flower_fact: '{new_flower_fact}'")
    print(f"    Fact: '{similarity['text']}': Similarity: {similarity['similarity']:.2f}")
