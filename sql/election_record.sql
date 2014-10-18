drop table election_record;
create table election_record(
election_id varchar not null,
area varchar,
no integer,
name varchar not null,
sec_name varchar,
gender varchar,
birth_year integer,
party varchar,
vote_cnt integer,
vote_rate real,
elect_ind boolean,
incumbent_Ind boolean,
primary key  (election_id,name,sec_name)
);
