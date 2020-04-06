# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_just_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 5cd4738202154452854991b2714ce49459316371
# Perfective
# Perfective :build_perfective_regex()
(LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|indentation(s)?|style|todo(s)?|typo(s)?|verbosity)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|indentation(s)?|style|todo(s)?|typo(s)?|verbosity)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))', '')))
 )
