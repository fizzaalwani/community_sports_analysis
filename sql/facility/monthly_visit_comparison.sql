-- august and july visits with facility
SELECT 
    f.facility_name, 
    
    SUM(CASE 
        WHEN d.full_date >= '2026-07-01' 
         AND d.full_date < '2026-08-01'
        THEN 1 ELSE 0 
    END) AS july_visits,
        
    SUM(CASE
        WHEN d.full_date >= '2026-08-01' 
         AND d.full_date < '2026-09-01' 
        THEN 1 ELSE 0 
    END) AS august_visits,
        
    (
        (
            SUM(CASE
                WHEN d.full_date >= '2026-08-01' 
                 AND d.full_date < '2026-09-01' 
                THEN 1 ELSE 0 
            END) 
            - 
            SUM(CASE 
                WHEN d.full_date >= '2026-07-01' 
                 AND d.full_date < '2026-08-01'
                THEN 1 ELSE 0 
            END)
        ) 
        / 
        SUM(CASE
            WHEN d.full_date >= '2026-08-01' 
             AND d.full_date < '2026-09-01' 
            THEN 1 ELSE 0 
        END) 
        * 100
    ) AS growth
        
FROM fact_attendance a 
INNER JOIN dim_date d 
    ON a.date_key = d.date_key
INNER JOIN dim_facility f 
    ON f.facility_key = a.facility_key

WHERE d.full_date >= '2026-07-01' 
  AND d.full_date < '2026-09-01'

GROUP BY f.facility_name;
