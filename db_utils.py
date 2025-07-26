# db_utils.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # change if you set one
        database="baymax"     # use your own db name
    )

def save_result(table: str, data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cols = ", ".join(data.keys())
    placeholders = []
    values = []
    for val in data.values():
        if isinstance(val, str) and val == "CURRENT_TIMESTAMP()":
            placeholders.append(val)  # raw SQL, no placeholder
        else:
            placeholders.append("%s")
            values.append(val)

    sql = f"INSERT INTO {table} ({cols}) VALUES ({', '.join(placeholders)})"
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
