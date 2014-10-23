\copy votecash to '/home/aha/Project/VoteCash/data/votecash.csv' with CSV HEADER;
\copy election to '/home/aha/Project/VoteCash/data/election.csv' with CSV HEADER;
\copy election_attr to '/home/aha/Project/VoteCash/data/election_attr.csv' with CSV HEADER;
\copy election_record to '/home/aha/Project/VoteCash/data/election_record.csv' with CSV HEADER;
\copy vote2election to '/home/aha/Project/VoteCash/data/vote2election.csv' with CSV HEADER;
\copy abt01 to '/home/aha/Project/VoteCash/data/abt01.csv' with CSV HEADER;

--  VIEW
\copy (select *,case when main_type in ('直轄市里長','總統','直轄市長','村里長','縣市長','鄉鎮市長') then 1 else 0 end as Leader_Ind,case when main_type='總統' then 1 when main_type='立法委員' then 2 when main_type='直轄市長' then 3 when main_type='直轄市議員' then 4 when main_type='縣市長' then 5 when main_type='縣市議員' then 6 when main_type='鄉鎮市長' then 7 when main_type='鄉鎮市民代表' then 8 when main_type='直轄市里長' then 9 when main_type='村里長' then 10 else 11 end as Position_Level from votemart order by vote_id) to '/home/aha/Project/VoteCash/data/votemart.csv' with CSV HEADER;
