# See "The Corrective Commit Probability Code Quality Metric" for the classifier MLE method
# https://arxiv.org/abs/2007.10912

CREATE OR REPLACE FUNCTION
general.bq_ccp_mle
 (base_prob FLOAT64)
 RETURNS FLOAT64
AS (
# Function version: 113a57f9a9cc811a84256910855c256b73c3668a
# Model version: 113a57f9a9cc811a84256910855c256b73c3668a
1.205*base_prob -0.048
 )
;


WITH tab AS (
  SELECT  0.0 AS prob
            , -0.048 as expected
    UNION ALL SELECT 1.0
                    , 1.157

    UNION ALL SELECT 0.1
                    , 0.07250000000000001

    UNION ALL SELECT null
                    , null
)
SELECT prob
, expected
, general.bq_ccp_mle(prob) as actual
, general.bq_ccp_mle(prob) = expected as pass
FROM tab as testing
;



CREATE OR REPLACE FUNCTION
general.bq_refactor_mle
 (base_prob FLOAT64)
 RETURNS FLOAT64
AS (
# Function version: 113a57f9a9cc811a84256910855c256b73c3668a
# Model version: 113a57f9a9cc811a84256910855c256b73c3668a
1.724*base_prob -0.034
 )
;

WITH tab AS (
  SELECT  0.0 AS prob
            , -0.034 as expected
    UNION ALL SELECT 1.0
                    , 1.69

    UNION ALL SELECT 0.1
                    , 0.1384

    UNION ALL SELECT null
                    , null
)
SELECT prob
, expected
, general.bq_refactor_mle(prob) as actual
, general.bq_refactor_mle(prob) = expected as pass
FROM tab as testing
;