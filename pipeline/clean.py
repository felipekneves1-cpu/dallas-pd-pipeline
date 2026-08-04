"""
clean.py

Cleans the incidents DataFrame loaded from the Dallas PD database:
converts date types and fixes known data-quality issues.
"""

import pandas as pd

# Values that are valid, expected categories for grand_jury_disposition.
# Anything outside this set gets replaced with 'Unknown' (e.g. the
# 'Redden, Craig W/M' value, which looks like a name that leaked into
# the wrong column in the original source).
VALID_DISPOSITIONS = {"No Bill", "True Bill", "Pending", "See Summary"}


def clean_incidents(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the incidents DataFrame: convert date column to datetime
    and normalize invalid grand_jury_disposition values.

    Args:
        df (pd.DataFrame): raw incidents DataFrame from load_table()

    Returns:
        pd.DataFrame: cleaned copy of the incidents DataFrame
    """
    df = df.copy()  # avoid mutating the original DataFrame in place

    # Convert 'date' from text to real datetime dtype.
    # errors='coerce' means: if any value can't be parsed as a date,
    # turn it into NaT (Not a Time) instead of crashing the program.
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Replace any grand_jury_disposition value that isn't in our
    # known valid set (including None/NaN) with 'Unknown'.
    df["grand_jury_disposition"] = df["grand_jury_disposition"].apply(
        lambda value: value if value in VALID_DISPOSITIONS else "Unknown"
    )

    return df