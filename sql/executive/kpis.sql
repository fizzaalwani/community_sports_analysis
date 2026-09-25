-- for month of july total members , active members , new members of the month , 
-- total visits of the month , revenue generated of the month
select count(member_key) as total_members, count(distinct CASE when join_date > '{month_start}' and
join_date < '{month_end}' THEN member_key END) as new_members, count(distinct  CASE when 
status='active' THEN member_key END) as active_members from dim_member


