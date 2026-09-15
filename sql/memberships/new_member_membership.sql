-- new members membership type
SELECT
    COUNT(*) AS new_members,

    COUNT(CASE
        WHEN membership_type = 'monthly'
        THEN 1
    END) AS monthly_members,

    COUNT(CASE
        WHEN membership_type = 'quarterly'
        THEN 1
    END) AS quarterly_members,


    COUNT(CASE
        WHEN membership_type = 'annual'
        THEN 1
    END) AS annual_members

FROM dim_member

WHERE join_date >= '2026-08-01'
  AND join_date < '2026-09-01';
  