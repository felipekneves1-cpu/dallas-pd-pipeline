"""
visualize.py

One function per chart. Each function accepts the DataFrame produced
by the corresponding analyze.py function and returns a matplotlib
Figure. Functions do not call plt.show() themselves -- main.py
decides whether to display or save the figure.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_incidents_by_weapon(df: pd.DataFrame):
    """
    Bar chart: incident count by subject weapon (Question 1).

    Args:
        df (pd.DataFrame): output of analyze_incidents_by_weapon()

    Returns:
        matplotlib.figure.Figure: the generated bar chart
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    df_sorted = df.sort_values("incident_count", ascending=True)
    ax.barh(df_sorted["subject_weapon"], df_sorted["incident_count"], color="#1F5C4E")
    ax.set_xlabel("Incident-subject pairs")
    ax.set_title("Incidents by Subject Weapon (2003-2016)")
    fig.tight_layout()
    return fig


def plot_incidents_by_year(df: pd.DataFrame):
    """
    Line chart: number of incidents per year (Question 2).

    Args:
        df (pd.DataFrame): output of analyze_incidents_by_year()

    Returns:
        matplotlib.figure.Figure: the generated line chart
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["year"], df["incident_count"], marker="o", color="#1F5C4E")
    ax.set_xlabel("Year")
    ax.set_ylabel("Incident count")
    ax.set_title("Officer-Involved Shootings by Year (2016 is partial)")
    fig.tight_layout()
    return fig


def plot_incidents_by_month(df: pd.DataFrame):
    """
    Bar chart: distribution of incidents by calendar month (Question 3).

    Args:
        df (pd.DataFrame): output of analyze_incidents_by_month()

    Returns:
        matplotlib.figure.Figure: the generated bar chart
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["month"], df["incident_count"], color="#1F5C4E")
    ax.set_xlabel("Month")
    ax.set_ylabel("Incident count")
    ax.set_title("Incident Distribution by Month (all years combined)")
    fig.tight_layout()
    return fig


def plot_yearly_trend_with_ranking(df: pd.DataFrame):
    """
    Combo chart: cumulative incident total over time (Question 4).

    Args:
        df (pd.DataFrame): output of analyze_yearly_trend_with_ranking()

    Returns:
        matplotlib.figure.Figure: the generated line chart
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["year"], df["cumulative_total"], marker="o", color="#1F5C4E")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative incident total")
    ax.set_title("Cumulative Officer-Involved Shootings (2003-2016)")
    fig.tight_layout()
    return fig