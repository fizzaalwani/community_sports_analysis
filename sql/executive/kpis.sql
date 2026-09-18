-- for month of july total members , active members , new members of the month , 
-- total visits of the month , revenue generated of the month
select count(member_key) as total_members, count(distinct CASE when join_date > '2026-06-01' and
join_date < '2026-07-01' THEN member_key END) as new_members, count(distinct  CASE when 
status='active' THEN member_key END) as active_members from dim_member


