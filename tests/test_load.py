"""
test_load.py

Minimal unit test for pipeline.load, confirming the incidents table
loads with the expected real shape.
"""

from pipeline.load import load_table


def test_load_incidents_shape():
    """
    Confirm that load_table('incidents') returns the known real
    shape of the incidents table (219 rows, 15 columns).
    """
    df = load_table("incidents")
    assert df.shape == (219, 15)