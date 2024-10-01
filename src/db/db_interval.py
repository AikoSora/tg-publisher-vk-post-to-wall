from sqlite3 import Error

from logging import error

from typing import TYPE_CHECKING
from typing import Optional

import sqlite3

if TYPE_CHECKING:
    from sqlite3 import Connection


DB_FILE = "user_states.db"


def create_connection() -> Optional['Connection']:
    """
    Function to create connection to sqlite database
    """

    try:
        return sqlite3.connect(DB_FILE)
    except Error as ex:
        error(ex)

    return None


def execute_sql_query(query: str, *args):
    """
    Function to execute sql query

    :param query: str
    """

    conn = create_connection()

    if conn is None:
        return error("Connection is not successfull")

    cursor = conn.cursor()

    cursor.execute(query, args)

    conn.commit()
    conn.close()


def create_table():
    """
    Function to create user_states table in database
    """

    execute_sql_query("""
    CREATE TABLE IF NOT EXISTS user_states (
        user_id INTEGER PRIMARY KEY,
        time_interval TEXT
    )
    """)


def delay_post_table():
    """
    Function to create delay_post table in database
    """

    execute_sql_query("""
    CREATE TABLE IF NOT EXISTS delay_post (
        user_id INTEGER PRIMARY KEY,
        time_post INTEGER
    )
    """)


def get_time_interval(user_id):
    """
    Function to get time_interval from user_states tables with user_id

    :param user_id: int
    :return str:
    """

    conn = create_connection()

    if conn is None:
        return error('Connection is not successfull')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT time_interval FROM user_states WHERE user_id=?",
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else error('Failed get time_interval variable')


def set_time_interval(user_id: int, time_interval: str):
    """
    Function to set time interval in database

    :param user_id: int
    :param time_interval: str
    """

    execute_sql_query(
        "REPLACE INTO user_states (user_id, time_interval) VALUES (?, ?)",
        user_id,
        time_interval,
    )


__all__ = (
    'create_connection',
    'execute_sql_query',
    'create_table',
    'delay_post_table',
    'get_time_interval',
    'set_time_interval',
)
