"""
test_clean.py

Minimal unit test for pipeline.clean, confirming that invalid
grand_jury_disposition values get normalized to 'Unknown'.
"""

from pipeline.load import load_table
from pipeline.clean import clean_incidents, VALID_DISPOSITIONS


def test_clean_disposition_only_valid_categories():
    """
    Confirm that after cleaning, grand_jury_disposition only contains
    values from VALID_DISPOSITIONS plus 'Unknown'.
    """
    df = load_table("incidents")
    df_clean = clean_incidents(df)
    allowed = VALID_DISPOSITIONS | {"Unknown"}
    assert set(df_clean["grand_jury_disposition"].unique()).issubset(allowed)