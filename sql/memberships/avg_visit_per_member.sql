SELECT
    m.membership_type,

    COUNT(DISTINCT m.member_key) AS members,

    COUNT(a.attendance_key) AS total_visits,

    ROUND(
        COUNT(a.attendance_key) /
        COUNT(DISTINCT m.member_key),
        2
    ) AS average_visits_per_member

FROM dim_member m

LEFT JOIN fact_attendance a
    ON m.member_key = a.member_key

LEFT JOIN dim_date d
    ON a.date_key = d.date_key
    AND d.full_date >= '{month_start}'
    AND d.full_date < '{month_end}'

WHERE m.status = 'Active'

GROUP BY m.membership_type

ORDER BY average_visits_per_member DESC;

