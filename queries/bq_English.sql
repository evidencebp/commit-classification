# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_English
 (message string)
 RETURNS int64
AS (
# Model language based on commit: d32ccba
# English
# English :build_English_regex()
(LENGTH(REGEXP_REPLACE(lower(message),'(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(about|all|also|and|because|but|can|come|could|day|even|find|first|for|from|get|give|have|her|here|him|his|how|into|its|just|know|like|look|make|man|many|more|new|not|now|one|only|other|our|out|people|say|see|she|some|take|tell|than|that|the|their|them|then|there|these|they|thing|think|this|those|time|two|use|very|want|way|well|what|when|which|who|will|with|would|year|you|your)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(about|all|also|and|because|but|can|come|could|day|even|find|first|for|from|get|give|have|her|here|him|his|how|into|its|just|know|like|look|make|man|many|more|new|not|now|one|only|other|our|out|people|say|see|she|some|take|tell|than|that|the|their|them|then|there|these|they|thing|think|this|those|time|two|use|very|want|way|well|what|when|which|who|will|with|would|year|you|your)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)', '')))
 )
