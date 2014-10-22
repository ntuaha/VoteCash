drop table mapping_vote2elect;
create table mapping_vote2elect(
year integer,
term integer,
elect_type varchar,
county varchar,
district varchar,
village varchar,
position varchar,
unique (year,county,district,village,position)
);
