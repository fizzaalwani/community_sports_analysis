-- Which facilities are most used by male and female members?
with cte as(
SELECT
    m.gender,
    f.facility_name,
    COUNT(a.attendance_key) AS total_visits
FROM fact_attendance a
JOIN dim_member m
    ON a.member_key = m.member_key
JOIN dim_facility f
    ON a.facility_key = f.facility_key
JOIN dim_date d
    ON a.date_key = d.date_key
WHERE d.full_date >= '{month_start}'
  AND d.full_date < '{month_end}'
GROUP BY
    m.gender,
    f.facility_name
ORDER BY
    m.gender,
    total_visits DESC
    ), ranked as (
select *, dense_rank() over(partition by gender order by total_visits desc) as rnk from cte
)

select * from ranked where rnk =1
    