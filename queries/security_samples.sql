# Commits
drop table if exists general.commit_security;


create table
general.commit_security
as
select
commit
, repo_name
, message
, general.bq_security(message) as is_security_pred
from
general.enhanced_commits
where
general.bq_security(message) > 0
;


# Secusity hits
select
repo_name
, commit
, message
, '' as Is_Security
, '' as Justification
, '' as Certain
, '' as Comment
, '22_jan_2021_pos_hits_36fdf4aea9d8dc83bdea98239b601ac51d07e5d9' as Sampling
from
general.commit_security
where
is_security_pred > 0
#and
#regexp_contains(lower(message), 'best')
order by
rand()
limit 500
;

# Terms related
WITH terms AS (
  SELECT SPLIT(message, ' ' ) as token
  FROM (  SELECT lower(message) as message
 FROM
 general.commit_security
 #where
 #general.bq_security(message) > 0
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, max(general.bq_security(word)) is_identified
, count(*) as cnt
FROM terms, UNNEST(token) as word
group by
word
#having
#max(general.bq_security(word)) > 0
order by count(*) desc
limit 1000
;
