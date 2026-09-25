WITH day_usage AS (
    SELECT
        m.gender,
        d.day_name,
        d.day_of_week,
        COUNT(a.attendance_key) AS total_visits
    FROM fact_attendance a
    JOIN dim_member m
        ON a.member_key = m.member_key
    JOIN dim_date d
        ON a.date_key = d.date_key
    WHERE d.full_date >= '{month_start}'
      AND d.full_date < '{month_end}'
    GROUP BY
        m.gender,
        d.day_name,
        d.day_of_week
)

SELECT
    gender,
    day_name,
    total_visits
FROM day_usage
WHERE (gender, total_visits) IN (
    SELECT gender, MAX(total_visits)
    FROM day_usage
    GROUP BY gender
);
