import psycopg2
import pandas as pd


async def create_connection(params):
    """
    Create a new connection with the postgreSQL
    database
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
        print(db_version)

        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        return None, None, True, str(error)


def close_connection(cur, conn):
    """
     Close the connection with the postgreSQL database
    """
    try:
        cur.close()
        if conn is not None:
            conn.close()
            print('Database connection closed')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def pg_to_pd(cur, query, columns):
    """
    Return the select result as panda dataframe
    """
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        return 1

    tupples = cur.fetchall()

    df = pd.DataFrame(tupples, columns=columns)
    return df