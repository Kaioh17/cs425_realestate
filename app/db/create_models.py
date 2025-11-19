from psycopg2 import Error
import psycopg2
from connect import connect_db

class create_tables:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur 

    def entities(self):
        print("table is been created")
        create_table = """ 
            CREATE TABLE IF NOT EXISTS users (
                user_id uuid PRIMARY KEY,
                role varchar,
                name varchar, 
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """
        self.cur.execute(create_table)
        self.conn.commit()

connect_= connect_db()
tables =create_tables(connect_.conn, connect_.cur)
tables.entities()
connect_.close_db()