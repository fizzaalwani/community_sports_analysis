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

WHERE join_date >= '{month_start}'
  AND join_date < '{month_end}';
  