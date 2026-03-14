from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Example functions
def get_user():
    return {"user": "Pavan"}

def get_orders():
    return {"orders": [101,102,103]}

def get_products():
    return {"products": ["Laptop","Phone"]}


@app.get("/data")
def get_all_data():

    with ThreadPoolExecutor(max_workers=3) as executor:

        future_user = executor.submit(get_user)
        future_orders = executor.submit(get_orders)
        future_products = executor.submit(get_products)

        user = future_user.result()
        orders = future_orders.result()
        products = future_products.result()

    return {
        "user": user,
        "orders": orders,
        "products": products
    }
#===============================
# Fast api to get query, vector search, external api
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
import time

app = FastAPI()

executor = ThreadPoolExecutor(max_workers=5)

# ---- Example functions ----

def get_user_from_db():
    time.sleep(2)   # simulate DB call
    return {"user_id": 1, "name": "Pavan"}

def vector_search():
    time.sleep(3)   # simulate vector DB search
    return {"documents": ["Doc1", "Doc2", "Doc3"]}

def external_api():
    time.sleep(2)
    return {"weather": "Cloudy"}


# ---- API endpoint ----

@app.get("/search")
def search():

    future_db = executor.submit(get_user_from_db)
    future_vector = executor.submit(vector_search)
    future_api = executor.submit(external_api)

    db_result = future_db.result()
    vector_result = future_vector.result()
    api_result = future_api.result()

    return {
        "user": db_result,
        "vector_results": vector_result,
        "external_data": api_result
    }
#=========================
#get multiple api's data
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
import requests

app = FastAPI()

# Create a global thread pool
executor = ThreadPoolExecutor(max_workers=5)

# Function to call external API
def fetch_api(url):
    response = requests.get(url)
    return response.json()


@app.get("/external-data")
def get_external_data():

    urls = [
        "https://jsonplaceholder.typicode.com/users/1",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/todos/1"
    ]

    futures = [executor.submit(fetch_api, url) for url in urls]

    results = [future.result() for future in futures]

    return {
        "user": results[0],
        "post": results[1],
        "todo": results[2]
    }
