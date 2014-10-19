drop table election_record;
create table election_record(
election_id varchar not null,
area varchar,
no integer,
name varchar not null,
gender varchar,
birth_year integer,
sec_name varchar,
sec_gender varchar,
sec_birth_year integer,
party varchar,
vote_cnt integer,
vote_rate real,
elect_ind boolean,
incumbent_Ind boolean,
primary key  (area,election_id,name,party)
);
