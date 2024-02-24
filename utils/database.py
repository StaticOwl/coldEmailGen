import psycopg2
import psycopg2.extras as pet


class DatabaseObject:

    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect_postgres(self):
        try:
            with psycopg2.connect(**self.config) as conn:
                print('Connected to the PostgreSQL database...')
                self.conn = conn
                self.cursor = conn.cursor(cursor_factory=pet.RealDictCursor)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_conn_cursor(self):
        return self.conn, self.cursor

    def query_to_commit(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def query_to_get_data(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_postgress(self):
        try:
            self.cursor.close()
            self.conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
