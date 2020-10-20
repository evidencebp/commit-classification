# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_refactor
 (message string)
 RETURNS int64
AS (
# Model language based on commit: a8cf9c3e9b738c22b16936caeeffe6583d1397b5
# Refactor
general.bq_positive_refactor(message)
 - general.bq_non_code_refactor(message)
 - general.bq_non_positive_linguistic_refactor(message)
 - general.bq_non_positive_linguistic_refactor_goals(message)
 - general.bq_non_positive_linguistic_refactor_removal(message)
 - general.bq_documentation_entities_context_refactor(message)
# Refactor - end
 )
 ;
