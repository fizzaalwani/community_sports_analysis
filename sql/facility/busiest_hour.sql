SELECT
    HOUR(check_in_time) AS hour_of_day,
    COUNT(*) AS total_visits

FROM fact_attendance a

JOIN dim_date d
    ON a.date_key = d.date_key

WHERE d.full_date >= '2026-08-01'
  AND d.full_date < '2026-09-01'

GROUP BY HOUR(check_in_time)

ORDER BY total_visits DESC
LIMIT 3