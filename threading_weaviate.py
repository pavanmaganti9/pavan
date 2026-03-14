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
#======================================
# Production example
import weaviate
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

# CONFIG
MAX_WORKERS = 8
BATCH_SIZE = 50

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Weaviate
client = weaviate.connect_to_local()

collection = client.collections.get("Documents")

# Example dataset (simulate large dataset)
documents = [f"Document content {i}" for i in range(10000)]

# Queue for storing embedding results
embedding_queue = Queue()


# STEP 1: EMBEDDING FUNCTION
def generate_embedding(text):

    vector = model.encode(text).tolist()

    embedding_queue.put({
        "text": text,
        "vector": vector
    })


# STEP 2: BATCH WRITER
def batch_writer():

    buffer = []

    while True:

        item = embedding_queue.get()

        if item is None:
            break

        buffer.append(item)

        if len(buffer) >= BATCH_SIZE:

            with collection.batch.dynamic() as batch:

                for obj in buffer:
                    batch.add_object(
                        properties={"text": obj["text"]},
                        vector=obj["vector"]
                    )

            print(f"Inserted batch of {len(buffer)}")

            buffer = []

    # Insert remaining
    if buffer:

        with collection.batch.dynamic() as batch:

            for obj in buffer:
                batch.add_object(
                    properties={"text": obj["text"]},
                    vector=obj["vector"]
                )

        print(f"Inserted final batch {len(buffer)}")


# STEP 3: START BATCH THREAD
writer_thread = threading.Thread(target=batch_writer)
writer_thread.start()


# STEP 4: MULTITHREADED EMBEDDINGS
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    executor.map(generate_embedding, documents)


# STOP WRITER
embedding_queue.put(None)
writer_thread.join()

print("All documents processed successfully")
