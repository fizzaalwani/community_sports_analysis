SELECT
    HOUR(check_in_time) AS hour_of_day,
    COUNT(*) AS total_visits

FROM fact_attendance a

JOIN dim_date d
    ON a.date_key = d.date_key

WHERE d.full_date >= '{month_start}'
  AND d.full_date < '{month_end}'

GROUP BY HOUR(check_in_time)

ORDER BY total_visits DESC
LIMIT 1