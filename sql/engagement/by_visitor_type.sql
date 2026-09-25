SELECT
    CASE
        WHEN visit_count = 1 THEN 'One-time visitor'
        WHEN visit_count BETWEEN 2 AND 4 THEN 'Occasional visitor'
        WHEN visit_count BETWEEN 5 AND 9 THEN 'Regular visitor'
        ELSE 'Frequent visitor'
    END AS visitor_type,

    COUNT(*) AS member_count

FROM (
    SELECT
        a.member_key,
        COUNT(*) AS visit_count

    FROM fact_attendance a

    JOIN dim_date d
        ON a.date_key = d.date_key

    WHERE d.full_date >= '{month_start}'
      AND d.full_date < '{month_end}'

    GROUP BY a.member_key
) x

GROUP BY visitor_type
ORDER BY member_count DESC;

