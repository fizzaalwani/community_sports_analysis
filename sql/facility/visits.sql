SELECT
    f.facility_name,

    COUNT(a.attendance_key) AS total_visits,

    ROUND(
        COUNT(a.attendance_key) * 100.0 /
        SUM(COUNT(a.attendance_key)) OVER (),
        2
    ) AS percentage_of_total_visits

FROM fact_attendance a

JOIN dim_facility f
    ON a.facility_key = f.facility_key

JOIN dim_date d
    ON a.date_key = d.date_key

WHERE d.full_date >= '2026-07-01'
  AND d.full_date < '2026-08-01'

GROUP BY f.facility_name

ORDER BY total_visits DESC;

