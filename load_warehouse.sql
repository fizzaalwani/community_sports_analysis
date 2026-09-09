-- 9. LOAD FACILITY DIMENSION
INSERT INTO dim_facility (
    facility_id,
    facility_name,
    capacity,
    hourly_rate_pkr
)
SELECT DISTINCT
    facility_id,
    TRIM(facility_name),
    capacity,
    hourly_rate_pkr
FROM staging_facilities;



-- 10. LOAD MEMBER DIMENSION
INSERT INTO dim_member (
    member_id,
    member_name,
    gender,
    age,
    membership_type,
    preferred_facility,
    join_date,
    expiry_date,
    status
)
SELECT
    member_id,
    TRIM(member_name),
    gender,
    age,
    membership_type,
    TRIM(preferred_facility),
    join_date,
    expiry_date,
    status
FROM (
    SELECT
        m.*,
        ROW_NUMBER() OVER (
            PARTITION BY member_id
            ORDER BY expiry_date DESC
        ) AS rn
    FROM staging_members m
) AS deduped
WHERE rn = 1;


-- 11. LOAD ATTENDANCE FACT
INSERT INTO fact_attendance (
    member_key,
    facility_key,
    date_key,
    check_in_time,
    visit_count
)
SELECT
    m.member_key,
    f.facility_key,
    CAST(DATE_FORMAT(a.attendance_date, '%Y%m%d') AS UNSIGNED),
    a.check_in_time,
    1
FROM (
    SELECT
        member_id,
        attendance_date,
        TRIM(facility) AS facility_clean,
        check_in_time,
        ROW_NUMBER() OVER (
            PARTITION BY
                member_id,
                attendance_date,
                TRIM(facility),
                check_in_time
            ORDER BY member_id
        ) AS rn
    FROM staging_attendance
    WHERE member_id IS NOT NULL
      AND facility IS NOT NULL
) AS a
JOIN dim_member m
    ON m.member_id = a.member_id
JOIN dim_facility f
    ON UPPER(TRIM(f.facility_name))
       = UPPER(a.facility_clean)
WHERE a.rn = 1;


-- 12. LOAD PAYMENT FACT
INSERT INTO fact_payment (
    member_key,
    date_key,
    payment_type,
    payment_status,
    amount_pkr
)
SELECT
    m.member_key,
    CAST(DATE_FORMAT(p.payment_date, '%Y%m%d') AS UNSIGNED),
    p.payment_type,
    p.payment_status,
    p.amount_pkr
FROM (
    SELECT
        p.*,
        ROW_NUMBER() OVER (
            PARTITION BY
                member_id,
                payment_date,
                amount_pkr,
                payment_type,
                payment_status
            ORDER BY member_id
        ) AS rn
    FROM staging_payments p
    WHERE amount_pkr IS NOT NULL
) AS p
JOIN dim_member m
    ON m.member_id = p.member_id
WHERE p.rn = 1;