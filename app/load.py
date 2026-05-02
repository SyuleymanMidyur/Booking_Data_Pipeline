from db_connection import get_connection


def get_last_loaded_timestamp():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT last_loaded_at 
        FROM pipeline_metadata 
        WHERE pipeline_name = 'orders_pipeline';
    """)

    result = cursor.fetchone()
    conn.close()

    return result[0]


def update_last_loaded_timestamp(new_timestamp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pipeline_metadata
        SET last_loaded_at = %s
        WHERE pipeline_name = 'orders_pipeline';
    """, (new_timestamp,))

    conn.commit()
    conn.close()



from psycopg2.extras import execute_batch
from db_connection import get_connection


def insert_raw_orders(orders):
    if not orders:
        print("No new orders to insert.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO raw_orders (id, user_id, amount, order_date, status)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    values = [
        (
            order["id"],
            order["user_id"],
            order["amount"],
            order["order_date"],
            order["status"]
        )
        for order in orders
    ]

    execute_batch(cursor, insert_query, values)

    conn.commit()
    conn.close()

    print(f"{len(values)} orders inserted.")