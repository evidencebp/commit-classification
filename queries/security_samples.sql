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
, is_corrective
from
general.enhanced_commits
where
general.bq_security(message) > 0
;


# Security fixes hits
select
repo_name
, commit
, message
, '' as Is_Security
, '' as Is_Fix
, '' as Is_Security_Fix
, '' as Justification
, '' as Certain
, '' as Comment
, '24_mar_2021_pos_fix_2be15899b72484a3927b01a57b476cf6e8b76188' as Sampling
from
general.commit_security
where
is_security_pred > 0
and
is_corrective
#and
#regexp_contains(lower(message), 'time')
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
