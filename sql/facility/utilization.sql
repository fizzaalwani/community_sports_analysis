-- utilization rate of facilites
SELECT 
    f.facility_name,

    COUNT(a.check_in_time) AS visits,

    28 * 10 AS assumed_capacity_hours,

    ROUND(
        (COUNT(a.check_in_time) / (28 * 10)) * 100,
        2
    ) AS utilization

FROM fact_attendance a

INNER JOIN dim_facility f 
    ON a.facility_key = f.facility_key

INNER JOIN dim_date d 
    ON d.date_key = a.date_key

WHERE d.full_date >= '{month_start}'
  AND d.full_date < '{month_end}'

GROUP BY f.facility_name;