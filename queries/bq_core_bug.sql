# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_core_bug
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 77a2f4fecd385d89b071264bb1f7c697da42924e
# Core Bug Term
(LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(bug(s|z)?|bug(-|\\s)?fix(es)?|defect(s)?|error(s)?|failur(ing|e|es|ed)|fault(s)?|fix(ed|es|ing)?|fixing(s)?|incorrect(ly)?|mistake(s|n|nly)?|problem(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(bug(s|z)?|bug(-|\\s)?fix(es)?|defect(s)?|error(s)?|failur(ing|e|es|ed)|fault(s)?|fix(ed|es|ing)?|fixing(s)?|incorrect(ly)?|mistake(s|n|nly)?|problem(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '')))
#Core Bug Term - end
 )
 ;
