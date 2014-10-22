\copy votecash to '/home/aha/Project/VoteCash/data/votecash.csv' with CSV HEADER;
\copy election to '/home/aha/Project/VoteCash/data/election.csv' with CSV HEADER;
\copy election_attr to '/home/aha/Project/VoteCash/data/election_attr.csv' with CSV HEADER;
\copy election_record to '/home/aha/Project/VoteCash/data/election_record.csv' with CSV HEADER;
\copy vote2election to '/home/aha/Project/VoteCash/data/vote2election.csv' with CSV HEADER;
\copy abt01 to '/home/aha/Project/VoteCash/data/abt01.csv' with CSV HEADER;

--  VIEW
\copy (select * from votemart order by vote_id) to '/home/aha/Project/VoteCash/data/votemart.csv' with CSV HEADER;
