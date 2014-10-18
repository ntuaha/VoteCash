drop table election_attr;
create table election_attr(
election_id varchar primary key,
area  varchar,
population  integer,
election_cnt  integer,
candidate_cnt integer,
candidate_male  integer,
candidate_female  integer,
winner_cnt  integer,
winner_male integer,
winner_female integer,
vote_cnt  integer,
vote_valid  integer,
vote_invalid  integer,
elect_pop_rate  real,
vote_elect_rate real,
cand_win_rate real
);
