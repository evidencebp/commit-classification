
select
repo_name
, count(distinct commit) as commits
, 1.0*count(distinct if(general.bq_cc_message(message) > 0, commit, null))/count(distinct commit) as cc_ratio
from
general.enhanced_commits
where
extract(year from commit_timestamp) = 2020
group by
repo_name
having
1.0*count(distinct if(general.bq_cc_message(message) > 0, commit, null))/count(distinct commit)  > 0.1
and count(distinct commit) >= 200
order by
1.0*count(distinct if(general.bq_cc_message(message) > 0, commit, null))/count(distinct commit) desc
;