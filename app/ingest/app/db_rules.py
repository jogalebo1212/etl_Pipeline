import psycopg2
import pandas as pd
from sql_queries import drop_table_queries, fill_table_queries, create_table_queries, create_constraints

class Db_engine:
    def create_connection(params):
        """
         Create a new connection with the postgreSQL
         database using the password, username, etc...
         and return the cur and conn object
        """
        conn = None

        try:
            print('Connecting to the PostgreSQL database')
            conn = psycopg2.connect(**params)
            conn.set_session(autocommit=True)

            cur = conn.cursor()

            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            db_version = cur.fetchone()
            print('Version of database: '+db_version)
            return cur, conn
        except (Exception, psycopg2.DatabaseError) as error:

            print(error)


    def close_connection(cur, conn):
        """
         Close the connection with the postgreSQL database
        """
        try:
            cur.close()
            if conn is not None:
                conn.close()
                print('Database connection is closed')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def drop_table(cur, conn, table):
        """
         Drop our table csv
        """

        query = "DROP TABLE IF EXISTS {0}".format(table)
        print(f"Executing: {query}")
        cur.execute(query)
        conn.commit()


    def drop_tables(cur, conn):
        """
         Drop all the tables in the example
        """
        print("Dropping tables")
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables dropped")


    def create_tables(cur, conn):
        """
        Create all the tables in the example
        """
        print("Creating created")
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables created")


    def pg_to_pd(cur, query, columns):
        """
         Return the select result as panda dataframe
         We could do it with pyspark but represents
         use he spark instances that make the problem
         more difficult but it could be more scalable
        """
        try:
            cur.execute(query)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            return 1

        tupples = cur.fetchall()

        df = pd.DataFrame(tupples, columns=columns)
        return df


    def fill_from_staging_all(cur, conn):
        """
         Fill all the records in the table
        """
        for query in fill_table_queries:
            cur.execute(query)
            conn.commit()
        print("Records were populated from staging")


    def check_data(cur, conn, tables):
        """
         Check how many records we get in tables
        """

        count_values = {}

        for table in tables:
            query_count = "SELECT COUNT(*) FROM {0}".format(table)

            try:
                cur = conn.cursor()
                cur.execute(query_count)
                count_values[table] = cur.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                raise

        return count_values


    def set_staging(cur, conn, staging_file, columns):
        """
        Set up the staging zone
        """
        print("Copying data from .csv to staging zone")

        try:
            copy_cmd = f"copy staging({','.join(columns)}) from stdout (format csv)"
            with open(staging_file, 'r') as f:
                next(f)
                cur.copy_expert(copy_cmd, f)
            conn.commit()
            print("Staging ready")
        except (psycopg2.Error) as e:
            print(e)


    def set_constraints(cur, conn):
        """
        Set up the constraints in our query
        """
        print("Setting constraints")
        for query in create_constraints:
            cur.execute(query)
            conn.commit()
        print("Constraints ready")
