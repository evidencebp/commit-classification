import sys
CODE_PATH = "C:/Idan/GitHub/in-work/lang"
sys.path.append(CODE_PATH)

import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from confusion_matrix import ConfusionMatrix, sk_to_grouped_df

@pytest.mark.parametrize(('classifier'
                         , 'concept'
                         , 'count'
                         , 'g_df'
                          , 'expected')
    , [
                             pytest.param(
                                 'classifier'
                                 , 'concept'
                                 , 'count'
                                 , pd.DataFrame([(True, True, 3)
                                       , (True, False, 4)
                                       , (False, True, 7)
                                       , (False, False, 16)]
                                   , columns=['classifier', 'concept', 'count'])
                                 , {'true_positives': 3, 'true_negatives': 16, 'false_positives': 4,
                                    'false_negatives': 7, 'samples': 30, 'accuracy': 0.633, 'positive_rate': 0.333,
                                    'hit_rate': 0.233, 'precision': 0.429, 'precision_lift': 0.286, 'recall': 0.3, 'fpr': 0.2,
                                    'jaccard': 0.214, 'comment': None}
                                 , id='regular1')
     ])
def test_summrize(classifier
                         , concept
                         , count
                         , g_df
                          , expected):
    cm = ConfusionMatrix(classifier
                         , concept
                         , count
                         , g_df
                         , digits=3)
    actual = cm.summarize()
    assert expected == actual




def test_sk_to_grouped_df():
    labels = [1,1,1,0,0,1]
    predictions = [1,1,0,0,0,0]
    actual = sk_to_grouped_df(labels=labels
                     , predictions=predictions)



    expected = pd.DataFrame([(0, 0, 2)
                                       , (1, 0, 2)
                                       , (1, 1, 2)]
                                   , columns=['concept', 'classifier', 'count'])
    assert_frame_equal(expected, actual)
