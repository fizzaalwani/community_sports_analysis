-- visits and revenue growth 
SELECT
    current_month.total_visits AS august_visits,
    previous_month.total_visits AS july_visits,

    ROUND(
        (current_month.total_visits - previous_month.total_visits)
        * 100.0 / NULLIF(previous_month.total_visits, 0),
        2
    ) AS visit_growth_percentage,

    current_month.revenue AS august_revenue,
    previous_month.revenue AS july_revenue,

    ROUND(
        (current_month.revenue - previous_month.revenue)
        * 100.0 / NULLIF(previous_month.revenue, 0),
        2
    ) AS revenue_growth_percentage

FROM

(
    SELECT
        COUNT(*) AS total_visits,

        (
            SELECT COALESCE(SUM(p.amount_pkr), 0)
            FROM fact_payment p
            JOIN dim_date d2
                ON p.date_key = d2.date_key
            WHERE d2.full_date >= '2026-08-01'
              AND d2.full_date < '2026-09-01'
              AND p.payment_status = 'paid'
        ) AS revenue

    FROM fact_attendance a
    JOIN dim_date d
        ON a.date_key = d.date_key

    WHERE d.full_date >= '2026-08-01'
      AND d.full_date < '2026-09-01'
) current_month

CROSS JOIN

(
    SELECT
        COUNT(*) AS total_visits,

        (
            SELECT COALESCE(SUM(p.amount_pkr), 0)
            FROM fact_payment p
            JOIN dim_date d2
                ON p.date_key = d2.date_key
            WHERE d2.full_date >= '2026-07-01'
              AND d2.full_date < '2026-08-01'
              AND p.payment_status = 'paid'
        ) AS revenue

    FROM fact_attendance a
    JOIN dim_date d
        ON a.date_key = d.date_key

    WHERE d.full_date >= '2026-07-01'
      AND d.full_date < '2026-08-01'
) previous_month;