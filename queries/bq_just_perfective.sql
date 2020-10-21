# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_just_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: fd01abaffc30965f113a30bc97e9a83d9beec50d
# Just Perfective
# Perfective :build_perfective_regex()
(LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|indentation(s)?|style|todo(s)?|typo(s)?|verbosity)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|indentation(s)?|style|todo(s)?|typo(s)?|verbosity)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '')))
 )
 ;