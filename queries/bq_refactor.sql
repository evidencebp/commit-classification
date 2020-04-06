# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_refactor
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 5cd4738202154452854991b2714ce49459316371
# Refactor
ccp.bq_positive_refactor(message)
 - ccp.bq_non_code_refactor(message)
 - ccp.bq_non_positive_linguistic_refactor(message)
 - ccp.bq_non_positive_linguistic_refactor_goals(message)
 - ccp.bq_non_positive_linguistic_refactor_removal(message)
 - ccp.bq_documentation_entities_context_refactor(message)
# Refactor - end
 )
