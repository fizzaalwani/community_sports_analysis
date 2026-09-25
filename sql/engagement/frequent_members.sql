-- new members membership type

SELECT
    m.member_id,
    m.member_name,
    m.membership_type,

    COUNT(a.attendance_key) AS visits

FROM dim_member m

LEFT JOIN fact_attendance a
    ON m.member_key = a.member_key

LEFT JOIN dim_date d
    ON a.date_key = d.date_key

WHERE  d.month_number = '{month}' and d.year ='{year}' and m.status = 'Active'

GROUP BY
    m.member_id,
    m.member_name,
    m.membership_type
ORDER by visits desc
limit 5