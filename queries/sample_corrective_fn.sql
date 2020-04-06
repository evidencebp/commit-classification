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
# Filter Addaptive hits
and ccp.bq_adaptive(message) = 0
# Filter corrective hits
and ccp.bq_corrective(message) = 0
and ccp.bq_refactor(message) = 0
# Random sampling with a constant seed
and rand() < 0.1
limit 5000