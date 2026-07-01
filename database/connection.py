import sqlite3

import pandas as pd

import streamlit as st

from utils.constants import DB_PATH


@st.cache_resource
def get_connection():

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def execute_query(query, params=()):

    conn = get_connection()

    return pd.read_sql_query(
        query,
        conn,
        params=params
    )