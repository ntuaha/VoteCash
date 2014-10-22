drop view  Votemart;
create view Votemart as select
A.Vote_id,
A.election_id,
B.r1,
B.r2,
B.r3,
B.r4,
B.r5,
B.r6,
B.p1,
B.p2,
B.p3,
B.p4,
B.p5,
B.p6,
B.p7,
B.p8,
B.p9,
B.p10,
B.r1+ B.r2+ B.r3+ B.r4+ B.r5+ B.r6  as income,
B.p1+ B.p2+ B.p3+ B.p4+ B.p5+ B.p6+ B.p7+ B.p8+ B.p9+ B.p10 as cost,
C.area,
C.no,
C.name,
C.gender,
C.birth_year,
C.sec_name,
C.sec_gender,
C.sec_birth_year,
C.party,
C.vote_cnt,
C.vote_rate,
C.elect_ind,
C.incumbent_Ind,
D.year,
D.term,
D.title,
D.main_type,
D.sub_type 
from vote2election A 
left join votecash B on A.vote_id = B.vote_id
left join election_record  C on A.election_id = C.election_id and A.name = C.name
left join election D on A.election_id = D.election_id
;


