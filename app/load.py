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