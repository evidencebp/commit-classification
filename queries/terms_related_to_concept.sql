WITH terms AS (
  SELECT id
        , title
        , SPLIT(title, ' ' ) as doc
  FROM ( SELECT 1 as id, 'few words' AS title
UNION ALL SELECT 2, 'here is a sentence with few words'
UNION ALL SELECT 3, 'the quick fox jumped over the lazy dog'
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, count(*) as cnt
FROM terms, UNNEST(doc) as word
group by
word
order by count(*) desc
;



select
word
, cnt
, general.bq_core_good(word) > 0 as in_core
from (
SELECT
     REGEXP_EXTRACT(message, r'([a-z0-9\._]*)') as word
     , count(*) as cnt
FROM (
 SELECT message
 FROM
 general.enhanced_commits
 where
 general.bq_good(message) > 0
)
GROUP BY
word
order by
count(*) desc
)
;


WITH terms AS (
  SELECT SPLIT(message, ' ' ) as token
  FROM (  SELECT lower(message) as message
 FROM
 general.enhanced_commits
 where
 general.bq_positive_sentiment(message) > 0
)
)
-- we flatten the ngrams into a table, and JOIN to our names
SELECT word
, max(general.bq_positive_sentiment(word)) is_identified
, count(*) as cnt
FROM terms, UNNEST(token) as word
group by
word
having
max(general.bq_positive_sentiment(word)) > 0
order by count(*) desc
limit 1000
;
