# Commits
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
, '11_jan_2021_pos_hits_040fdcc30ddd8fcc119b99151a74f8f4f2fa53a3' as Sampling
from
general.commit_sentiment
where
is_positive > 0
#and
#regexp_contains(lower(message), 'best')
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
, '11_jan_2021_neg_hits_040fdcc30ddd8fcc119b99151a74f8f4f2fa53a3' as Sampling
from
general.commit_sentiment
where
is_negative > 0
order by
rand()
limit 500
;

# PR comments
drop table if exists general.pr_comments_sentiment;


create table
general.pr_comments_sentiment
as
select
pull_request_id
, comment_id
, body
, general.bq_positive_sentiment(body) as is_positive
, general.bq_negative_sentiment(body) as is_negative
from
general_ght.pull_request_comments
where
general.bq_positive_sentiment(body) > 0
or
general.bq_negative_sentiment(body) > 0
;

select
count(*)
, sum(if(is_positive > 0, 1,0)) as positives
, sum(if(is_negative > 0, 1,0)) as negatives
from
general.pr_comments_sentiment
;

# Positive sentiment hits
select
pull_request_id
, comment_id
, body
, '' as Is_Positive
, '' as Is_Negative
, '' as Justification
, '' as Certain
, '' as Comment
, '11_jan_2021_pr_pos_hits_040fdcc30ddd8fcc119b99151a74f8f4f2fa53a3' as Sampling
from
general.pr_comments_sentiment
where
is_positive > 0
#and
#regexp_contains(lower(message), 'best')
order by
rand()
limit 500
;


# Negative sentiment hits
select
pull_request_id
, comment_id
, body
, '' as Is_Positive
, '' as Is_Negative
, '' as Justification
, '' as Certain
, '' as Comment
, '11_jan_2021_pr_neg_hits_040fdcc30ddd8fcc119b99151a74f8f4f2fa53a3' as Sampling
from
general.pr_comments_sentiment
where
is_negative > 0
order by
rand()
limit 500
;