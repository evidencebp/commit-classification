# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_adaptive
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_adaptive
(LENGTH(REGEXP_REPLACE(lower(message),'^(feat|build|chore|ci|test|perf)(\\(.*\\))?(!)?:', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'^(feat|build|chore|ci|test|perf)(\\(.*\\))?(!)?:', '')))
# cc_adaptive - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_corrective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_corrective
(LENGTH(REGEXP_REPLACE(lower(message),'^(fix)(\\(.*\\))?(!)?:', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'^(fix)(\\(.*\\))?(!)?:', '')))
# cc_corrective - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_refactor
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_refactor
(LENGTH(REGEXP_REPLACE(lower(message),'^(refactor)(\\(.*\\))?(!)?:', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'^(refactor)(\\(.*\\))?(!)?:', '')))
# cc_refactor - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_just_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_just_perfective
(LENGTH(REGEXP_REPLACE(lower(message),'^(docs|style)(\\(.*\\))?(!)?:', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'^(docs|style)(\\(.*\\))?(!)?:', '')))
# cc_just_perfective - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_perfective
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_perfective
(LENGTH(REGEXP_REPLACE(lower(message),'(^(refactor)(\\(.*\\))?(!)?:|^(docs|style)(\\(.*\\))?(!)?:)', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(^(refactor)(\\(.*\\))?(!)?:|^(docs|style)(\\(.*\\))?(!)?:)', '')))
# cc_perfective - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_cc_message
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 60af4655d2baeb3aa15768a02cacf0bff5612e2b
# cc_message
(LENGTH(REGEXP_REPLACE(lower(message),'(^(feat|build|chore|ci|test|perf|fix|docs|style|docs|style)(\\(.*\\))?(!)?:|breaking\\s+change(!)?:)', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(^(feat|build|chore|ci|test|perf|fix|docs|style|docs|style)(\\(.*\\))?(!)?:|breaking\\s+change(!)?:)', '')))
# cc_message - end
 )
 ;
