"""
load.py

Responsible for connecting to the Dallas PD SQLite database and
retrieving data, either as a full table or as the result of a
custom SQL query.
"""

import sqlite3
from pathlib import Path
import pandas as pd


def get_db_path() -> Path:
    """
    Build the absolute path to the SQLite database file, regardless
    of which folder the script is run from.

    Args:
        None

    Returns:
        Path: absolute path to data/dallas-ois.sqlite
    """
    # __file__ is this script's own location (pipeline/load.py)
    # .parent goes up to the project root (dallas_pd_pipeline/)
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "data" / "dallas-ois.sqlite"


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load an entire table from the Dallas PD database into a DataFrame.

    Args:
        table_name (str): name of the table to load
                           ('incidents', 'officers', or 'subjects')

    Returns:
        pd.DataFrame: full contents of the requested table
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


def run_query(query: str) -> pd.DataFrame:
    """
    Run an arbitrary SQL query against the Dallas PD database
    (used for the JOIN / GROUP BY / CTE / window function questions).

    Args:
        query (str): a full SQL query string

    Returns:
        pd.DataFrame: result of the query
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn)
    conn.close()
    return df