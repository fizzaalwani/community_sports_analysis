SELECT
    engagement_level,
    COUNT(*) AS member_count,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM
(
    SELECT
        m.member_id,

        COUNT(a.attendance_key) AS visits,

        CASE
            WHEN COUNT(a.attendance_key) >= 20
                THEN 'Highly Active'

            WHEN COUNT(a.attendance_key) >= 10
                THEN 'Regular'

            WHEN COUNT(a.attendance_key) >= 3
                THEN 'Low Engagement'

            ELSE 'Inactive'
        END AS engagement_level

    FROM dim_member m

    LEFT JOIN fact_attendance a
        ON m.member_key = a.member_key

    LEFT JOIN dim_date d
        ON a.date_key = d.date_key
        AND d.full_date >= '2026-07-01'
        AND d.full_date < '2026-08-01'

    WHERE m.status = 'active'

    GROUP BY m.member_id
) engagement

GROUP BY engagement_level

ORDER BY member_count DESC;

