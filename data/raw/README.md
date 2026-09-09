# Community Sports Complex — Synthetic ETL Dataset

Synthetic data created for a portfolio/consulting proof-of-concept.

## Files

- `members.csv` — membership master data
- `attendance.csv` — facility attendance/check-in records
- `payments.csv` — membership payments
- `facilities.csv` — facility master/reference data

## Deliberately messy data

The dataset contains a small number of:
- duplicate attendance/payment records
- inconsistent capitalization/whitespace
- missing payment amount
- inconsistent facility names

These are intentional so the ETL pipeline can demonstrate data cleaning and validation.

## Suggested ETL

CSV files
→ Extract
→ Clean/standardize
→ Validate
→ Join
→ PostgreSQL
→ Analytical SQL
→ BI dashboard

## Suggested dashboard KPIs

- Total members
- Active members
- Expired memberships
- Renewal rate
- Total revenue
- Monthly revenue
- Total visits
- Most popular facility
- Facility utilization
- Peak attendance hours
- Attendance by month
- Revenue by membership type

All names and records are fictional and contain no real personal data.
