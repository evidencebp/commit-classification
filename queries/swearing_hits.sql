# Pull request hits
# into pull_request_swearing_hits.csv
Select
*
, '' as Is_Swearing
from
general_ght.pull_request_comments
where
general.bq_swearing(body) > 0
;

# Commits hits
# into commits_swearing_hits.csv
Select
*
, '' as Is_Swearing
from
general.enhanced_commits
where
general.bq_swearing(message) > 0
order by
rand()
limit 1000
;