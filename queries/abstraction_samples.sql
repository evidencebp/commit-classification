select
count(*) as commits
, count(distinct repo_name) as repos
from
general.enhanced_commits
where
general.bq_abstraction(message) > 0
;

# Abstraction hits
select
repo_name
, commit
, message
, '' as Is_abstraction
, '' as Justification
, '' as Certain
, '' as Comment
, '14_jan_2021_abstraction_047d51716e9324e5a574e35eb3c75475da55bc5a' as Sampling
from
general.enhanced_commits
where
general.bq_abstraction(message) > 0
#and
#regexp_contains(lower(message), 'best')
order by
rand()
limit 500
;



WITH terms AS (
  SELECT SPLIT(message, ' ' ) as token
  FROM (  SELECT lower(message) as message
 FROM
 general.enhanced_commits
 where
 general.bq_abstraction(message) > 0
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, max(general.bq_abstraction(word)) is_identified
, count(*) as cnt
FROM terms, UNNEST(token) as word
group by
word
having
max(general.bq_abstraction(word)) > 0
order by count(*) desc
limit 1000
;
