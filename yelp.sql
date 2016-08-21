create table business (
  business_id varchar(50) primary key,
  name_desc varchar(200) not null,
  neighborhoods varchar(200),
  full_address varchar(200) not null,
  city varchar(50) not null,
  state varchar(50) not null,
  latitude number(8),
  longitude number(8),
  stars number(8),
  review_count number(8),
  categories varchar(200),
  open_bool varchar(50),
  type_desc varchar(50)
);
alter table business
  drop column latitude;
alter table business
  drop column longitude;
alter table business
  drop column categories;
alter table business
  drop column type_desc;
alter table business
  drop column neighborhoods;
------------------------------------------------------------------------------------------------------
-- Populated using categories.py
create table categories (
  business_id varchar(50),
  category varchar(50),
  constraint categories_pk primary key (business_id, category),
  constraint categories_business_id_fk foreign key (business_id) references business(business_id)
);
-------------------------------------------------------------------------------------------------------
-- Friends column removed from dataset using OpenOffice spreadsheet
create table yelp_user (
  yelping_since varchar(50),
  compliments_plain number(8),
  review_count number(10,2),
  compliments_cute number(10),
  compliments_writer number(8),
  fans number(8),
  compliments_note number(8),
  type_desc varchar(50),
  compliments_hot number(10),
  compliments_cool number(10),
  compliments_profile number(8),
  average_stars number(10,2),
  compliments_more number(8),
  elite varchar(100),
  name_desc varchar(100),
  user_id varchar(50) primary key,
  votes_cool number(20),
  compliments_list number(8),
  votes_funny number(8),
  compliments_photos number(8),
  compliments_funny number(8),
  votes_useful number(8)
);
alter table yelp_user
  drop column type_desc;
alter table yelp_user
  drop column elite;
-----------------------------------------------------------------------------------
-- Text column removed from dataset using review.py
create table review (
  user_id varchar(50),
  review_id varchar(50) primary key,
  votes_cool number(8),
  business_id varchar(50),
  votes_funny number(8),
  stars number(8),
  review_date varchar(50),
  type_desc varchar(10),
  votes_useful varchar(50),
  constraint business_id_fk foreign key (business_id) references business(business_id)
);
alter table review
  drop column type_desc;
alter table review
  add r_date date;
-- Dates in correct format added to table using date.py
alter table review
  drop column review_date;
alter table review
  rename column r_date to review_date;
----------------------------------------------------------------------------------------------
-- Text column in dataset replaced with tip_id numbers using tips.py
create table tips (
  user_id varchar(50),
  tip_id number(10) primary key,
  business_id varchar(50),
  likes number(8),
  tip_date  varchar(20),
  type_desc varchar(10)
);
alter table tips
  drop column type_desc;
alter table tips
  add t_date date;
-- dates in correct formant added using dates.py
alter table tips
  drop column tip_date;
alter table tips
  rename column t_date to tip_date;
