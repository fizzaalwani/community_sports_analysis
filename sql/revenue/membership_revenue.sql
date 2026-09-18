SELECT
    m.membership_type,

    COUNT(p.payment_key) AS payment_transactions,

    SUM(
        CASE
            WHEN p.payment_status = 'paid'
            THEN p.amount_pkr
            ELSE 0
        END
    ) AS revenue

FROM fact_payment p

JOIN dim_member m
    ON p.member_key = m.member_key

JOIN dim_date d
    ON p.date_key = d.date_key

WHERE d.full_date >= '2026-07-01'
  AND d.full_date < '2026-08-01'

GROUP BY m.membership_type

ORDER BY revenue DESC;
