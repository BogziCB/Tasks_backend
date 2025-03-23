import os
import sys
import time
from typing import List

import mariadb
from dotenv import load_dotenv

from api.response_model import Task

load_dotenv()

def connect():
    host = os.environ.get("DB_HOST")
    password = os.environ.get("DB_PASS")
    attempts = 10
    for i in range(attempts):
        try:
            # creates a connection object to the database and returns it
            conn = mariadb.connect(
                user="root",
                password=password,
                host=host,
                port=3306,
                database="tasks"
            )
            print('Connection to the database is successful!')
            return conn
        except Exception as e:
            print(f"Attempt {i+1}/{attempts}: Error connecting to MariaDB: {e}")
            time.sleep(2)

    print("Failed to connect after several attempts.")
    sys.exit(1)

def fetch_data():
    with connect() as conn:
        with conn.cursor() as cursor:
            content = []
            select_data ="""
                SELECT id, name, description, status
                FROM tasks
            """
            try:
                cursor.execute(select_data)
                for(id, name, description, status) in cursor:
                    result = {
                        "id": id,
                        "name": name,
                        "description": description,
                        "status": status
                    }
                    content.append(result)
                print("Data fetched")
                return content
            except Exception as e:
                print("Failed!")
                return False
def create_table():
    with connect() as conn:
        with conn.cursor() as cursor:
            print('Attempt to create the table if is not existent.')
            create_table_query = """
                CREATE TABLE IF NOT EXISTS tasks(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    description VARCHAR(255),
                    status VARCHAR(255)
                )
            """
            cursor.execute(create_table_query)
            print('Database exists or was created')


def add_task(task: Task):
    with connect() as conn:
        with conn.cursor() as cursor:
            print('Attempt to store task into DB.')
            insert_query = """
                INSERT INTO tasks(name, description,status)
                VALUES(?,?,"to do")
            """
            try:
                cursor.execute(insert_query, (task.name, task.description))
                conn.commit()
                print(f'Task {task.name} added')
                return True
            except Exception:
                print(f'Failed to store {task.name} into DB')
                return None

def update_task(id: int, task: Task):
    with connect() as conn:
        with conn.cursor() as cursor:
            print(f'Attempt to update task {id}')
            update_query = """
                UPDATE tasks
                SET name = ?, description = ?
                WHERE id = ?;
            """
            try:
                if task.status == 'to do' or task.status == 'in progress' or task.status == 'done':
                    cursor.execute(update_query, (task.name, task.description, id))
                    conn.commit()
                    return True
                else:
                    return "Forbidden"
            except Exception as e:
                print(f'Failed to update task {id}')
                return None

def update_status(id: int, status: str):
    with connect() as conn:
        with conn.cursor() as cursor:
            print(f'Attempt to update task {id}')
            update_query = """
                UPDATE tasks
                SET status = ?
                WHERE id = ?;
            """
            try:
                cursor.execute(update_query, (status, id))
                conn.commit()
                return True
            except Exception as e:
                print(f'Failed to update task {id}')
                return None

def delete_tasks(id: int):
    with connect() as conn:
        with conn.cursor() as cursor:
            print(f'Attempt to delete tasks {id}')
            delete_query = """
                DELETE FROM tasks
                WHERE id=?
            """
            try:
                cursor.execute(delete_query, (id,))
                conn.commit()
                return True
            except Exception as e:
                print("Failed to delete!")
                return False