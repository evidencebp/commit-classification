# Commits
drop table if exists general.commit_satd;


create table
general.commit_satd
as
select
commit
, repo_name
, message
, general.bq_satd(message) as is_satd_pred
, is_corrective
from
general.enhanced_commits
where
general.bq_satd(message) > 0
#regexp_contains(message, '(TODO|FIXME|HACK|XXX)')
;


# satd hits
select
repo_name
, commit
, message
, '' as Is_satd
, '' as Justification
, '' as Certain
, '' as Comment
, '23_dec_2021_pos_ee9407ac1244dca96f9b8e2bf2b5ac4fcea16ca2' as Sampling
from
general.commit_satd
where
is_satd_pred > 0
order by
rand()
limit 500
;

# Terms related
WITH terms AS (
  SELECT SPLIT(message, ' ' ) as token
  FROM (  SELECT lower(message) as message
 FROM
 general.commit_satd
 #where
 #general.bq_satd(message) > 0
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, max(general.bq_satd(word)) is_identified
, count(*) as cnt
FROM terms, UNNEST(token) as word
group by
word
#having
#max(general.bq_satd(word)) > 0
order by count(*) desc
limit 1000
;
