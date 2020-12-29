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
, '28_dec_2020_pos_hits_3334798837' as Sampling
from
general.commit_sentiment
where
is_positive > 0
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
, '28_dec_2020_neg_hits_3334798837' as Sampling
from
general.commit_sentiment
where
is_negative > 0
order by
rand()
limit 500
;