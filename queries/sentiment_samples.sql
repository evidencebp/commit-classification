drop table if exists general.commit_sentiment;


create table
general.commit_sentiment
as
select
commit
, repo_name
, message
, general.bq_positive_sentiment(message) as is_positive
, general.bq_negative_sentiment(message) as is_negative
from
general.enhanced_commits
where
general.bq_positive_sentiment(message) > 0
or
general.bq_negative_sentiment(message) > 0
;

select
count(*)
, sum(if(is_positive > 0, 1,0)) as positives
, sum(if(is_negative > 0, 1,0)) as negatives
from
general.commit_sentiment
;

# Positive sentiment hits
select
repo_name
, commit
, message
, '' as Is_Positive
, '' as Is_Negative
, '' as Justification
, '' as Certain
, '' as Comment
, '6_jan_2021_good_pos_hits_b471e816b55e8356a2d4c2ea3dcc851c68794f21' as Sampling
from
general.commit_sentiment
where
is_positive > 0
and
regexp_contains(lower(message), 'good')
order by
rand()
limit 500
;


# Negative sentiment hits
select
repo_name
, commit
, message
, '' as Is_Positive
, '' as Is_Negative
, '' as Justification
, '' as Certain
, '' as Comment
, '5_jan_2021_neg_hits_b471e816b55e8356a2d4c2ea3dcc851c68794f21' as Sampling
from
general.commit_sentiment
where
is_negative > 0
order by
rand()
limit 500
;