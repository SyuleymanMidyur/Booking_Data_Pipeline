from extract import extract_orders
from load import insert_raw_orders
from metadata import get_last_loaded_timestamp, update_last_loaded_timestamp


def run_pipeline():
    last_loaded = get_last_loaded_timestamp()
    orders = extract_orders()

    new_orders = [
        order for order in orders
        if order["order_date"] > last_loaded
    ]

    insert_raw_orders(new_orders)

    if new_orders:
        max_timestamp = max(order["order_date"] for order in new_orders)
        update_last_loaded_timestamp(max_timestamp)


if __name__ == "__main__":
    run_pipeline()