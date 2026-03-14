import weaviate
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Weaviate
client = weaviate.connect_to_local()

collection_name = "Documents"

# Example documents
documents = [
    "Python is a programming language",
    "Vector databases store embeddings",
    "Weaviate supports hybrid search",
    "Multithreading improves performance",
    "Embeddings convert text into vectors"
]


# Function to create embedding
def create_embedding(text):
    vector = model.encode(text).tolist()
    return {"text": text, "vector": vector}


# Run embedding generation concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(create_embedding, documents))


# Insert into Weaviate
collection = client.collections.get(collection_name)

for item in results:
    collection.data.insert(
        properties={"text": item["text"]},
        vector=item["vector"]
    )

print("All documents inserted successfully.")

#======================================
#adding in Batch
with collection.batch.dynamic() as batch:
    for item in results:
        batch.add_object(
            properties={"text": item["text"]},
            vector=item["vector"]
        )
