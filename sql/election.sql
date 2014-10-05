drop table election;
create table election(
election_id varchar PRIMARY KEY,
year integer,
term integer,
title varchar,
main_type varchar,
sub_type varchar,
election_dt timestamp
);
