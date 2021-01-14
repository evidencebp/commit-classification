# Positive sentiment hits
select
repo_name
, commit
, message
, '' as Is_abstraction
, '' as Justification
, '' as Certain
, '' as Comment
, '14_jan_2021_abstraction_' as Sampling
from
general.enhanced_commits
where
general.bq_abstraction > 0
#and
#regexp_contains(lower(message), 'best')
order by
rand()
limit 500
;
