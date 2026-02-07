from datetime import datetime
import random
import requests


def extract_orders():
    url = "https://dummyjson.com/carts"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch data")

    data = response.json()["carts"]

    orders = []

    for cart in data:
        order = {
            "id": cart["id"],
            "user_id": cart["userId"],
            "amount": cart["total"],
            "order_date": datetime.now(),
            "status": random.choice(["completed", "cancelled"])
        }
        orders.append(order)

    return orders