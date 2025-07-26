# db_connector.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # use your actual MySQL password if set
        database="baymax"
    )
