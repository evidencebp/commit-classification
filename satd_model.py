"""
A model for identifying Self Admitted Technical Debt (SATD)
"""

import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH, term_seperator
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier


# Using the list from
# An exploratory study on self-admitted technical debt by Potdar, Aniket and Shihab, Emad
positive_terms = ['fixme', 'hack', 'todo', 'xxx']

removal_terms = [
    'because'
    , 'clean' + REGULAR_SUFFIX
    , 'fix' + REGULAR_SUFFIX
    , 'implement' + REGULAR_SUFFIX
    , 'list' + REGULAR_SUFFIX
    , 'mov' + VERB_E_SUFFIX
    , 'remov' + VERB_E_SUFFIX
    , 'resolv' + VERB_E_SUFFIX
    , 'updat' + VERB_E_SUFFIX
    , 'was'
]
excluded_terms = ['update todo'
    , "(%s)%s(%s)" % ("|".join(removal_terms), NEAR_ENOUGH, "|".join(positive_terms))
    , "(%s)(/|\.|=)" % ("|".join(positive_terms))
    , '\.xxx'
    , '=xxx'
                  ]

def build_positive_regex():

    #return "(%s)" % ("|".join(positive_terms))

    return build_sepereted_term(positive_terms)



def build_excluded_regex():
    return "(%s)" % ("|".join(excluded_terms))
    #return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_satd(commit_text):
    #commit_text = re.sub(r"\s+", " ", commit_text.strip())
    text = commit_text.lower()

    return (len(re.findall(build_positive_regex(), text))
            - len(re.findall(build_excluded_regex(), text))
            - len(re.findall(build_not_positive_regex(), text)))  > 0



def satd_to_bq():
    concept = 'satd'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_satd(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_satd(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_satd(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):


    concepts = {'core_satd' : build_positive_regex
        , 'excluded_satd': build_excluded_regex
        , 'not_positive_satd' : build_not_positive_regex
        #, 'satd': satd_to_bq

                }

    for i in concepts.keys():
        print()
        print_func = lambda : print_logic_to_bq(regex_func=concepts[i]
                                                , concept=i)
        generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                            , concept=i)
                             , print_func
                             , commit=commit)
        print()

    generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                        , concept='satd')
                         , satd_to_bq
                         , commit=commit)
    print()
def evaluate_satd_classifier():

    evaluate_concept_classifier(concept='satd'
                                , text_name='message'
                                , classification_function=is_satd
                                , samples_file=join(DATA_PATH, 'satd_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='7bea7aa3de54a7763a52d93161615fe345483b19')
    evaluate_satd_classifier()

    text = """""Merge branch 'for-linus' of git://git.infradead.org/users/vkoul/slave-dma

Pull slave-dmaengine updates from Vinod Koul:
 ""For dmaengine contributions we have:
   - designware cleanup by Andy
   - my series moving device_control users to dmanegine_xxx APIs for
     later removal of device_control API
   - minor fixes spread over drivers mainly mv_xor, pl330, mmp, imx-sdma
     etc""

* 'for-linus' of git://git.infradead.org/users/vkoul/slave-dma: (60 commits)
  serial: atmel: add missing dmaengine header
  dmaengine: remove FSLDMA_EXTERNAL_START
  dmaengine: freescale: remove FSLDMA_EXTERNAL_START control method
  carma-fpga: move to fsl_dma_external_start()
  carma-fpga: use dmaengine_xxx() API
  dmaengine: freescale: add and export fsl_dma_external_start()
  dmaengine: add dmaengine_prep_dma_sg() helper
  video: mx3fb: use dmaengine_terminate_all() API
  serial: sh-sci: use dmaengine_terminate_all() API
  net: ks8842: use dmaengine_terminate_all() API
  mtd: sh_flctl: use dmaengine_terminate_all() API
  mtd: fsmc_nand: use dmaengine_terminate_all() API
  V4L2: mx3_camer: use dmaengine_pause() API
  dmaengine: coh901318: use dmaengine_terminate_all() API
  pata_arasan_cf: use dmaengine_terminate_all() API
  dmaengine: edma: check for echan->edesc => NULL in edma_dma_pause()
  dmaengine: dw: export probe()/remove() and Co to users
  dmaengine: dw: enable and disable controller when needed
  dmaengine: dw: always export dw_dma_{en,dis}able
  dmaengine: dw: introduce dw_dma_on() helper
  ...
"
""".lower()
    print("Label", is_satd(text))
    print("concept in text", re.findall(build_positive_regex(), text))
    print("exclusion in text", re.findall(build_excluded_regex(), text))
    #print(build_excluded_regex())
    #print("v1", re.findall("(because|clean(?:s|ed|ing)?|fix(?:s|ed|ing)?|implement(?:s|ed|ing)?|list(?:s|ed|ing)?|remov(?:e|es|ed|ing)|was)[\S\s]{0,40}", text))
