Select
distinct
repo_name
, commit
, message
from ccp.active_2019_commits
where
# Samples are used for model building, not estimation.
# Hence, we can restirct to shorter text and enable easier labeling
# without statiatical representation concerns
length(message) > 200
and length(message) > 0
# Focus in English texts
and ccp.bq_English(message) > 0
and ccp.bq_corrective(message) = 1
and substr(commit, 4,1) = 'c'
limit 5000