"""
main.py

Orchestrates the full pipeline: load -> clean -> analyze -> visualize.
Saves one PNG chart per analytical question into outputs/.
"""

from pathlib import Path

from pipeline.load import load_table
from pipeline.clean import clean_incidents
from pipeline.analyze import (
    analyze_incidents_by_weapon,
    analyze_incidents_by_year,
    analyze_incidents_by_month,
    analyze_yearly_trend_with_ranking,
)
from pipeline.visualize import (
    plot_incidents_by_weapon,
    plot_incidents_by_year,
    plot_incidents_by_month,
    plot_yearly_trend_with_ranking,
)


def main():
    """
    Run the full pipeline end to end and print a summary of each step.

    Args:
        None

    Returns:
        None
    """
    outputs_dir = Path(__file__).resolve().parent / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    # Load + clean (clean.py is mainly used here as a data-quality
    # check; the analytical queries run directly against the database
    # via analyze.py, which is why we load/clean separately).
    incidents_raw = load_table("incidents")
    incidents_clean = clean_incidents(incidents_raw)
    print(f"[load+clean] incidents: {incidents_raw.shape} -> cleaned: {incidents_clean.shape}")

    # Question 1
    df_weapon = analyze_incidents_by_weapon()
    print(f"[analyze] Q1 by weapon: {df_weapon.shape[0]} categories, "
          f"total incidents = {df_weapon['incident_count'].sum()}")
    fig1 = plot_incidents_by_weapon(df_weapon)
    fig1.savefig(outputs_dir / "q1_incidents_by_weapon.png", dpi=150)

    # Question 2
    df_year = analyze_incidents_by_year()
    print(f"[analyze] Q2 by year: total incidents = {df_year['incident_count'].sum()}")
    fig2 = plot_incidents_by_year(df_year)
    fig2.savefig(outputs_dir / "q2_incidents_by_year.png", dpi=150)

    # Question 3
    df_month = analyze_incidents_by_month()
    print(f"[analyze] Q3 by month: total incidents = {df_month['incident_count'].sum()}")
    fig3 = plot_incidents_by_month(df_month)
    fig3.savefig(outputs_dir / "q3_incidents_by_month.png", dpi=150)

    # Question 4
    df_ranking = analyze_yearly_trend_with_ranking()
    print(f"[analyze] Q4 cumulative + ranking: final cumulative = "
          f"{df_ranking['cumulative_total'].iloc[-1]}")
    fig4 = plot_yearly_trend_with_ranking(df_ranking)
    fig4.savefig(outputs_dir / "q4_cumulative_trend.png", dpi=150)

    print(f"\nAll 4 charts saved to {outputs_dir}")


if __name__ == "__main__":
    main()