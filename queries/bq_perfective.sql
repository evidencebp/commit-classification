# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: a8cf9c3e9b738c22b16936caeeffe6583d1397b5
# Perfective
general.bq_just_perfective(message)
 + general.bq_refactor(message)
# Perfective - end
 )
 ;
