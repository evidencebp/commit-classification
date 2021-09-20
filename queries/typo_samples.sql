# Commits
drop table if exists general.commit_typo;


create table
general.commit_typo
as
select
commit
, repo_name
, message
, general.bq_typo(message) as is_typo_pred
from
general.enhanced_commits
where
general.bq_typo(message) > 0
;


# Security fixes hits
select
repo_name
, commit
, message
, '' as Is_Typo
, '' as Justification
, '' as Certain
, '' as Comment
, '19_sep_2021_hit_81e7b2f240ba39adde3d6ece4030d144fce19d50' as Sampling
from
general.commit_typo
where
is_typo_pred > 0
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
 general.commit_typo
 #where
 #general.bq_typo(message) > 0
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, max(general.bq_typo(word)) is_identified
, count(*) as cnt
FROM terms, UNNEST(token) as word
group by
word
#having
#max(general.bq_typo(word)) > 0
order by count(*) desc
limit 1000
;
