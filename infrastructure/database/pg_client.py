import psycopg2
from psycopg2 import sql

class PostgreSQLClient:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def create_user_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                )
            """)
            self.conn.commit()

    def create_lesson_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS lesson (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    time timestamptz,
                    title VARCHAR(100),
                    video BYTEA,
                    transcript TEXT,
                    utterances TEXT,
                    assistant_id VARCHAR(100),
                    thread_id VARCHAR(100)
                )
            """)
            self.conn.commit()

    def insert_user(self, name, email):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            self.conn.commit()

    def get_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()

    def update_user(self, user_id, name, email):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
            self.conn.commit()

    def delete_user(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()

# Example Usage
client = PostgreSQLClient('postgres', 'postgres', 'mysecretpassword')
client.create_lesson_table()
