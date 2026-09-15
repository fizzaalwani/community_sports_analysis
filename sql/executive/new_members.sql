-- new members of the month
select count(a.member_key) as total_visits from fact_attendance a inner join dim_date d 
on a.date_key=d.date_key where d.month_number = 6 and d.year=2026 
