-- august and july visits with facility
SELECT 
    f.facility_name, 
    
    SUM(CASE 
        WHEN d.full_date >= '{previous_start}' 
         AND d.full_date < '{month_start}'
        THEN 1 ELSE 0 
    END) AS previous_month_visits,
        
    SUM(CASE
        WHEN d.full_date >= '{month_start}' 
         AND d.full_date < '{month_end}' 
        THEN 1 ELSE 0 
    END) AS current_month_visits,
        
    (
        (
            SUM(CASE
                WHEN d.full_date >= '{month_start}' 
                 AND d.full_date < '{month_end}' 
                THEN 1 ELSE 0 
            END) 
            - 
            SUM(CASE 
                WHEN d.full_date >= '{previous_start}' 
                 AND d.full_date < '{month_start}'
                THEN 1 ELSE 0 
            END)
        ) 
        / 
        SUM(CASE
            WHEN d.full_date >= '{month_start}' 
             AND d.full_date < '{month_end}' 
            THEN 1 ELSE 0 
        END) 
        * 100
    ) AS growth
        
FROM fact_attendance a 
INNER JOIN dim_date d 
    ON a.date_key = d.date_key
INNER JOIN dim_facility f 
    ON f.facility_key = a.facility_key

WHERE d.full_date >= '{previous_start}' 
  AND d.full_date < '{month_end}'

GROUP BY f.facility_name;
