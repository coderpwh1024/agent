import os
from openai import AzureOpenAI
import numpy as np
from dotenv import load_dotenv

load_dotenv()

endpoint=" "
deployment=" "
apiKey=" "


client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


text = 'the quick brown fox jumped over the lazy dog'
model = 'text-embedding-3-large'

client.embeddings.create(input=[text], model=model).data[0].embedding

automobile_embedding = client.embeddings.create(input='automobile', model=model).data[0].embedding
vehicle_embedding = client.embeddings.create(input='vehicle', model=model).data[0].embedding
dinosaur_embedding = client.embeddings.create(input='dinosaur', model=model).data[0].embedding
stick_embedding = client.embeddings.create(input='stick', model=model).data[0].embedding

print(cosine_similarity(automobile_embedding, automobile_embedding))
print(cosine_similarity(automobile_embedding, vehicle_embedding))
print(cosine_similarity(automobile_embedding, dinosaur_embedding))
print(cosine_similarity(automobile_embedding, stick_embedding))
