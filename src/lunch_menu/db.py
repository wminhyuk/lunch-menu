import psycopg
from dotenv import load_dotenv
import os
import pandas as pd
from psycopg.rows import dict_row

# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()

db_name = os.getenv("DB_NAME")
DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": os.getenv("DB_NAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
            }

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s);",
                (menu_name, member_id, dt)
                )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False

def select_table():
    query = """
    SELECT
        l.menu_name,
        m.name,
        l.dt
    FROM
        lunch_menu l
        inner join member m
        on l.member_id = m.id
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    #conn.commit()
    cursor.close()
    conn.close()
   
    df = pd.DataFrame(rows, columns=['menu', 'ename', 'dt'])
    return df

