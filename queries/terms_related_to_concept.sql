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