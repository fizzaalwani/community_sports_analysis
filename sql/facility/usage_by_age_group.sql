with cte as (
SELECT
    CASE
        WHEN m.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN m.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN m.age BETWEEN 36 AND 45 THEN '36-45'
        WHEN m.age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56+'
    END AS age_group,

    f.facility_name,

    COUNT(a.attendance_key) AS total_visits

FROM fact_attendance a

JOIN dim_member m
    ON a.member_key = m.member_key

JOIN dim_facility f
    ON a.facility_key = f.facility_key

JOIN dim_date d
    ON a.date_key = d.date_key

WHERE d.full_date >= '2026-07-01'
  AND d.full_date < '2026-08-01'

GROUP BY
    age_group,
    f.facility_name

ORDER BY
    age_group,
    total_visits DESC
    
    ), ranked as (
select * , dense_rank() over(partition by age_group order by total_visits desc) as rnk from cte
)
select * from ranked where rnk=1