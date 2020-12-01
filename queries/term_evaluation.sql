# Corrective
select
language
, r.repo_name as repo_name
, commit
, commit_timestamp
, subject
, message
, is_corrective
from
general.enhanced_commits as ec
join
general.repos as r
on
ec.repo_name = r.repo_name
where
regexp_contains(lower(message), '((assignment|assign|=) in if|== instead of =)')
and not is_corrective
order by
language
, r.repo_name
, commit_timestamp
;

select
count(*) as cases
, count(distinct commit) as commits
, count(distinct repo_name) as repositories
, avg(if(is_corrective, 1,0)) as corrective_rate
from
general.enhanced_commits as ec
where
regexp_contains(lower(message), '((assignment|assign|=) in if|== instead of =)')
;

# Refactor
select
language
, r.repo_name as repo_name
, commit
, commit_timestamp
, subject
, message
, is_refactor
from
general.enhanced_commits as ec
join
general.repos as r
on
ec.repo_name = r.repo_name
where
regexp_contains(lower(message), r'need(?:s|ing)?\srefactor(?:ing)?')
and is_refactor
order by
language
, r.repo_name
, commit_timestamp
;

select
count(*) as cases
, count(distinct commit) as commits
, count(distinct repo_name) as repositories
, avg(if(is_refactor, 1,0)) as refactor_rate
from
general.enhanced_commits as ec
where
regexp_contains(lower(message), r'need(?:s|ing)?\srefactor(?:ing)?')
;