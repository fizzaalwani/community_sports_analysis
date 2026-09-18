-- Show me all currently active members who have either never visited, or whose most recent
-- visit was before September 1, 2026."
SELECT
    m.member_id,
    m.member_name,
    m.membership_type,
    m.expiry_date,

    MAX(d.full_date) AS last_visit

FROM dim_member m

LEFT JOIN fact_attendance a
    ON m.member_key = a.member_key

LEFT JOIN dim_date d
    ON a.date_key = d.date_key

WHERE m.status = 'active'

GROUP BY
    m.member_id,
    m.member_name,
    m.membership_type,
    m.expiry_date

HAVING
    MAX(d.full_date) IS NULL
    OR MAX(d.full_date) < '2026-08-01'

ORDER BY
    last_visit;