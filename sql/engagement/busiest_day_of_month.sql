-- What was the single busiest day of the entire month?
SELECT
    d.full_date,
    d.day_name,
    COUNT(a.attendance_key) AS total_visits
FROM fact_attendance a
JOIN dim_date d
    ON a.date_key = d.date_key
WHERE d.full_date >= '2026-08-01'
  AND d.full_date < '2026-09-01'
GROUP BY
    d.full_date,
    d.day_name
ORDER BY total_visits DESC
LIMIT 1;
