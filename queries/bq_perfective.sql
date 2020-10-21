# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: fd01abaffc30965f113a30bc97e9a83d9beec50d
# Perfective
general.bq_just_perfective(message)
 + general.bq_refactor(message)
# Perfective - end
 )
 ;
