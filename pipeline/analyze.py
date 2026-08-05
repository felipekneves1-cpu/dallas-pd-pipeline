"""
analyze.py

One function per analytical question. Each function builds a SQL
query (using JOIN, date functions, CTEs, or window functions as
required) and runs it via pipeline.load.run_query().
"""

import pandas as pd
from pipeline.load import run_query


def analyze_incidents_by_weapon() -> pd.DataFrame:
    """
    Question 1 (Aggregation and Mapping): count of incidents and
    average number of officers involved, grouped by subject weapon.
    Uses JOIN + GROUP BY + aggregate functions.

    A CTE first reduces subjects to one row per case_number (its
    count of subjects), so the LEFT JOIN below neither duplicates
    incidents that have multiple subjects nor drops incidents that
    have none -- the result always sums to 219.

    Args:
        None

    Returns:
        pd.DataFrame: columns [subject_weapon, incident_count, avg_officers]
    """
    query = """
        WITH subject_counts AS (
            SELECT case_number, COUNT(*) AS n
            FROM subjects
            GROUP BY case_number
        )
        SELECT
            i.subject_weapon,
            COUNT(*) AS incident_count,
            AVG(i.officer_count) AS avg_officers
        FROM incidents i
        LEFT JOIN subject_counts sc ON i.case_number = sc.case_number
        GROUP BY i.subject_weapon
        ORDER BY incident_count DESC
    """
    return run_query(query)


def analyze_incidents_by_year() -> pd.DataFrame:
    """
    Question 2 (Time-Based Trend): number of incidents per year.
    Uses SQL date functions (strftime).

    Args:
        None

    Returns:
        pd.DataFrame: columns [year, incident_count]
    """
    query = """
        SELECT
            strftime('%Y', date) AS year,
            COUNT(*) AS incident_count
        FROM incidents
        GROUP BY year
        ORDER BY year
    """
    return run_query(query)


def analyze_incidents_by_month() -> pd.DataFrame:
    """
    Question 3 (Date Distribution): distribution of incidents by
    calendar month, across all years. Uses a CTE to extract the
    month before grouping.

    Args:
        None

    Returns:
        pd.DataFrame: columns [month, incident_count]
    """
    query = """
        WITH incidents_with_month AS (
            SELECT
                strftime('%m', date) AS month
            FROM incidents
        )
        SELECT
            month,
            COUNT(*) AS incident_count
        FROM incidents_with_month
        GROUP BY month
        ORDER BY month
    """
    return run_query(query)


def analyze_yearly_trend_with_ranking() -> pd.DataFrame:
    """
    Question 4 (Advanced Comparison): for each year, show the
    running cumulative total of incidents and the rank of that
    year by incident count. Uses window functions.

    Args:
        None

    Returns:
        pd.DataFrame: columns [year, incident_count, cumulative_total, rank_by_count]
    """
    query = """
        WITH yearly_counts AS (
            SELECT
                strftime('%Y', date) AS year,
                COUNT(*) AS incident_count
            FROM incidents
            GROUP BY year
        )
        SELECT
            year,
            incident_count,
            SUM(incident_count) OVER (ORDER BY year) AS cumulative_total,
            RANK() OVER (ORDER BY incident_count DESC) AS rank_by_count
        FROM yearly_counts
        ORDER BY year
    """
    return run_query(query)