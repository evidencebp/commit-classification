

CREATE OR REPLACE FUNCTION
general.bq_ccp_mle
 (base_prob FLOAT64)
 RETURNS FLOAT64
AS (
# Function version: 113a57f9a9cc811a84256910855c256b73c3668a
# Model version: 113a57f9a9cc811a84256910855c256b73c3668a
1.253*base_prob -0.053
 )
;

WITH tab AS (
  SELECT  0.0 AS prob
            , -0.053 as expected
    UNION ALL SELECT 1.0
                    , 1.2

    UNION ALL SELECT 0.1
                    , 0.0723

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
1.695*base_prob -0.034
 )
;

WITH tab AS (
  SELECT  0.0 AS prob
            , -0.034 as expected
    UNION ALL SELECT 1.0
                    , 1.661

    UNION ALL SELECT 0.1
                    , 0.1355

    UNION ALL SELECT null
                    , null
)
SELECT prob
, expected
, general.bq_refactor_mle(prob) as actual
, general.bq_refactor_mle(prob) = expected as pass
FROM tab as testing
;