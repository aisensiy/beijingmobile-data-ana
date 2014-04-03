drop table if exists locallist;
create table locallist (
  user_id bigint(64) primary key,
  locations text,
  location_size int,
  date date,
  gprs_flow double,
  gprs_fee double,
  call_fee double,
  brand_chn varchar(32),
  terminal_price int,
  dept_county_name varchar(64),
  dept_name varchar(64)
);
