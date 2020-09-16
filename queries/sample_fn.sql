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
, 'Not identified' as Sampling
from
general.enhanced_commits
where
length(message) > 0
and
length(message) <= 100
and
(not is_corrective and not is_adaptive and not is_perfective)
group by
repo_name
, commit
limit 1000
;