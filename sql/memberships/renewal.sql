-- renewal rate
 SELECT

    COUNT(*) AS memberships_expiring,

    SUM(
        CASE
            WHEN status = 'active'
            THEN 1
            ELSE 0
        END
    ) AS renewed_members,

    ROUND(
        SUM(
            CASE
                WHEN status = 'active'
                THEN 1
                ELSE 0
            END
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS renewal_rate

FROM dim_member
WHERE expiry_date >= '2026-07-01'
  AND expiry_date < '2026-08-01';