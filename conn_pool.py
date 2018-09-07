import sqlite3
# Singleton
__conn_pool = None


def get_connection():
    return __conn_pool


def release_conn(conn):
    return __conn_pool.close()


def start_conn_pool(dbname="scu_rm_acs"):
    global __conn_pool
    if __conn_pool is None:
        __conn_pool = sqlite3.connect(dbname)
        print("Connection pool started")
    else:
        print("connection pool already started!")
    pass
