# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 5cd4738202154452854991b2714ce49459316371
# Perfective
ccp.bq_just_perfective(message)
 + ccp.bq_refactor(message)
# Perfective - end
 )
