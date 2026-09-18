-- revenue of the month
select sum(p.amount_pkr) as revenue from fact_payment p inner join dim_date d 
on p.date_key=d.date_key where d.month_number = 6 and d.year =2026