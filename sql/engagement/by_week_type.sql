-- Are members primarily using the facility during working days or weekends?
SELECT
    CASE
        WHEN d.is_weekend = TRUE THEN 'Weekend'
        ELSE 'Weekday'
    END AS period_type,

    COUNT(a.attendance_key) AS total_visits,

    COUNT(DISTINCT a.member_key) AS unique_members

FROM fact_attendance a

JOIN dim_date d
    ON a.date_key = d.date_key

WHERE d.full_date >= '2026-08-01'
  AND d.full_date < '2026-09-01'

GROUP BY period_type;
