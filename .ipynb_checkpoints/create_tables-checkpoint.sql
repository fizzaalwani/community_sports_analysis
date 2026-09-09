CREATE DATABASE IF NOT EXISTS SportsComplexDW;

USE SportsComplexDW;



-- 1. STAGING TABLES
CREATE TABLE staging_members (
    member_id VARCHAR(20),
    member_name VARCHAR(100),
    gender VARCHAR(20),
    age INT,
    membership_type VARCHAR(30),
    preferred_facility VARCHAR(50),
    join_date DATE,
    expiry_date DATE,
    status VARCHAR(20)
);


CREATE TABLE staging_facilities (
    facility_id VARCHAR(20),
    facility_name VARCHAR(50),
    capacity INT,
    hourly_rate_pkr DECIMAL(10,2)
);

CREATE TABLE staging_attendance (
    member_id VARCHAR(20),
    attendance_date DATE,
    facility VARCHAR(50),
    check_in_time TIME
);


CREATE TABLE staging_payments (
    member_id VARCHAR(20),
    payment_date DATE,
    amount_pkr DECIMAL(10,2),
    payment_type VARCHAR(30),
    payment_status VARCHAR(20)
);



-- 2. DATE DIMENSION
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_month TINYINT NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_week TINYINT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    month_number TINYINT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter_num TINYINT NOT NULL,
    year SMALLINT NOT NULL
);


-- ============================================
-- 3. MEMBER DIMENSION
-- ============================================

CREATE TABLE dim_member (
    member_key INT AUTO_INCREMENT PRIMARY KEY,
    member_id VARCHAR(20) NOT NULL UNIQUE,
    member_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    age INT,
    membership_type VARCHAR(30),
    preferred_facility VARCHAR(50),
    join_date DATE,
    expiry_date DATE,
    status VARCHAR(20),
    is_current BOOLEAN DEFAULT TRUE,
    load_date DATETIME DEFAULT CURRENT_TIMESTAMP
);



-- 4. FACILITY DIMENSION
CREATE TABLE dim_facility (
    facility_key INT AUTO_INCREMENT PRIMARY KEY,
    facility_id VARCHAR(20) NOT NULL UNIQUE,
    facility_name VARCHAR(50) NOT NULL,
    capacity INT,
    hourly_rate_pkr DECIMAL(10,2)
);



-- 5. ATTENDANCE FACT
CREATE TABLE fact_attendance (
    attendance_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_key INT NOT NULL,
    facility_key INT NOT NULL,
    date_key INT NOT NULL,
    check_in_time TIME,
    visit_count INT DEFAULT 1,

    CONSTRAINT fk_attendance_member
        FOREIGN KEY (member_key)
        REFERENCES dim_member(member_key),

    CONSTRAINT fk_attendance_facility
        FOREIGN KEY (facility_key)
        REFERENCES dim_facility(facility_key),

    CONSTRAINT fk_attendance_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);


-- 6. PAYMENT FACT
CREATE TABLE fact_payment (
    payment_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_key INT NOT NULL,
    date_key INT NOT NULL,
    payment_type VARCHAR(30),
    payment_status VARCHAR(20),
    amount_pkr DECIMAL(10,2),

    CONSTRAINT fk_payment_member
        FOREIGN KEY (member_key)
        REFERENCES dim_member(member_key),

    CONSTRAINT fk_payment_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);



-- 7. INDEXES
CREATE INDEX idx_attendance_member
ON fact_attendance(member_key);

CREATE INDEX idx_attendance_facility
ON fact_attendance(facility_key);

CREATE INDEX idx_attendance_date
ON fact_attendance(date_key);

CREATE INDEX idx_payment_member
ON fact_payment(member_key);

CREATE INDEX idx_payment_date
ON fact_payment(date_key);



-- 8. POPULATE DATE DIMENSION
-- 2025-01-01 → 2027-12-31
SET SESSION cte_max_recursion_depth = 2000;
INSERT INTO dim_date (
    date_key,
    full_date,
    day_of_month,
    day_name,
    day_of_week,
    is_weekend,
    month_number,
    month_name,
    quarter_num,
    year
)
WITH RECURSIVE dates AS (
    SELECT DATE('2025-01-01') AS d

    UNION ALL

    SELECT DATE_ADD(d, INTERVAL 1 DAY)
    FROM dates
    WHERE d < DATE('2027-12-31')
)
SELECT
    CAST(DATE_FORMAT(d, '%Y%m%d') AS UNSIGNED) AS date_key,
    d AS full_date,
    DAY(d) AS day_of_month,
    DAYNAME(d) AS day_name,
    DAYOFWEEK(d) AS day_of_week,
    CASE
        WHEN DAYOFWEEK(d) IN (1,7) THEN TRUE
        ELSE FALSE
    END AS is_weekend,
    MONTH(d) AS month_number,
    MONTHNAME(d) AS month_name,
    QUARTER(d) AS quarter_num,
    YEAR(d) AS year
FROM dates;
