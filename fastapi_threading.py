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
