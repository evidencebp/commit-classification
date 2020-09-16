select
repo_name
, commit
, max(message) as message
, '' as Is_Refactor
, '' as Is_Perfective
, '' as Is_Adaptive
, '' as Is_Corrective
, '' as Justification
, '' as Comment
, '' as Certain
, 'random_batch_15_sep_2020' as Sampling
from
general.enhanced_commits
group by
repo_name
, commit
order by
rand()
limit 5000
;