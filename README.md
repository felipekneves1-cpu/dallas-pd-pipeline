# Dallas PD Officer-Involved Shootings – Data Pipeline (DS_202)

Modular Python + SQL pipeline analyzing Dallas Police Department officer-involved shooting incidents (2003–2016). Final project for DS_202 at Cornerstone International Community College of Canada (CICCC).

## Problem

How are officer-involved shooting incidents in Dallas distributed by subject weapon, year, and month, and how did the yearly totals evolve over time?

## Data

- Dallas PD officer-involved shootings dataset (2003–2016), stored as a SQLite database: `data/dallas-ois.sqlite`
- Tables: `incidents`, `officers`, `subjects` (linked by `case_number`)
- 219 incidents in total

**Cleaning applied (`clean.py`):**
- Converted the `date` column from text to datetime (invalid values become `NaT` instead of crashing)
- Normalized `grand_jury_disposition`: any value outside the valid set (`No Bill`, `True Bill`, `Pending`, `See Summary`) is replaced with `Unknown`. One example was a person's name that had leaked into this column in the original source.

## Structure

```
dallas-pd-pipeline/
├── data/                 # dallas-ois.sqlite
├── pipeline/
│   ├── load.py           # connects to SQLite; load_table() and run_query()
│   ├── clean.py          # clean_incidents()
│   ├── analyze.py        # one SQL query per question
│   └── visualize.py      # one matplotlib chart per question
├── tests/                # pytest unit tests (load, clean)
├── outputs/              # generated PNG charts (not committed)
├── .github/workflows/    # CI: runs tests on every push
└── main.py               # runs the full pipeline end to end
```

## Analytical Questions

| # | Question | SQL techniques |
|---|----------|----------------|
| 1 | Incidents and average officers involved, by subject weapon | CTE, LEFT JOIN, GROUP BY, aggregates |
| 2 | Incidents per year | Date functions (`strftime`) |
| 3 | Distribution of incidents by calendar month | CTE + date functions |
| 4 | Cumulative total per year and ranking of years by incident count | Window functions (`SUM() OVER`, `RANK() OVER`) |

## Challenges

**Symptom:** the weapon query (Q1) returned a total that did not match the 219 incidents in the database.

**Cause:** joining `incidents` directly to `subjects` duplicated incidents with more than one subject, and incidents with no subject record were lost.

**Fix:** a CTE first reduces `subjects` to one row per `case_number`, and a LEFT JOIN keeps every incident exactly once. The result now always sums to 219.

## How to Run

```bash
pip install -r requirements.txt
python main.py        # saves 4 charts to outputs/
pytest                # runs the unit tests
```

## Tools

Python, pandas, SQLite, SQL (CTEs, JOINs, window functions), matplotlib, pytest, GitHub Actions
