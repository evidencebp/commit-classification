"""

"""


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, NEAR_ENOUGH, VERB_E_SUFFIX
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
"""

positive_terms = [
    'better' + NEAR_ENOUGH + 'time(?:s)?',
    #'(cpu|gpu|tpu)',
    #'day(?:s)?',
    '(fast|faster|fastest)',
    #'hour(?:s)?',
    'improv' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    '(long|longer|short|shorter|above|least)' + NEAR_ENOUGH + 'time(?:s)?',
    #'minute(?:s)?',
    'optimis' + VERB_E_SUFFIX,
    'optimisation',
    'optimiz' + VERB_E_SUFFIX,
    'optimization',
    'performance',
    'reduc' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    #'second(?:s)?',
    '(speed|speeding)',
    'tak' + VERB_E_SUFFIX + NEAR_ENOUGH + 'time(?:s)?',
    #'run(?: |-)?time(?:s)?',
    '(slow|slower|slowest)',
    ]

excluded_terms = ['[a-z0-9/\.-]*fast/[a-z0-9/\.-]*',
                  'optimize imports', # Common as a command in IDEs like JetBrains
                  'performance suite(?:s)?',
                  'performance (testing|test|tests)',
                  'renam' + VERB_E_SUFFIX + NEAR_ENOUGH + 'fast',
                  'sometime(?:s)?',
                  '(unnoticed|found)' + NEAR_ENOUGH + 'long time',
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_performance(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def performance_to_bq():
    concept = 'performance'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_{concept}(message)".format(schema=SCHEMA_NAME
                                                       , concept=concept))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_{concept}(message)".format(schema=SCHEMA_NAME
                                                           , concept=concept))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_{concept}(message)".format(schema=SCHEMA_NAME
                                                               , concept=concept))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concept = 'performance'

    concepts = {'core_' + concept : build_positive_regex
        , 'excluded_' + concept : build_excluded_regex
        , 'not_positive_' + concept : build_not_positive_regex
        #, 'swearing': swearing_to_bq

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
                                                        , concept=concept)
                         , performance_to_bq
                         , commit=commit)
    print()
def evaluate_performance_classifier():

    evaluate_concept_classifier(concept='performance'
                                , text_name='message'
                                , classification_function=is_performance
                                , samples_file=join(DATA_PATH, 'commit_performance_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='a5655cab58c1e717c8dcf06bc754812fbba79a72')
    #evaluate_performance_classifier()

    text = """
"2009-02-23  Geoffrey Garen  <ggaren@apple.com>

        Reviewed by Sam Weinig.

        Next step in splitting JIT functionality out of the Interpreter class:
        Moved vptr storage from Interpreter to JSGlobalData, so it could be shared
        between Interpreter and JITStubs, and moved the *Trampoline JIT stubs
        into the JITStubs class. Also added a VPtrSet class to encapsulate vptr
        hacks during JSGlobalData initialization.
        
        SunSpider says 0.4% faster. Meh.

        * JavaScriptCore.exp:
        * JavaScriptCore.xcodeproj/project.pbxproj:
        * interpreter/Interpreter.cpp:
        (JSC::Interpreter::Interpreter):
        (JSC::Interpreter::tryCacheGetByID):
        (JSC::Interpreter::privateExecute):
        * interpreter/Interpreter.h:
        * jit/JIT.cpp:
        (JSC::JIT::privateCompileMainPass):
        (JSC::JIT::privateCompile):
        (JSC::JIT::privateCompileCTIMachineTrampolines):
        * jit/JIT.h:
        (JSC::JIT::compileCTIMachineTrampolines):
        * jit/JITCall.cpp:
        (JSC::JIT::compileOpCall):
        (JSC::JIT::compileOpCallSlowCase):
        * jit/JITPropertyAccess.cpp:
        (JSC::JIT::privateCompilePatchGetArrayLength):
        * jit/JITStubs.cpp:
        (JSC::JITStubs::JITStubs):
        (JSC::JITStubs::tryCacheGetByID):
        (JSC::JITStubs::cti_vm_dontLazyLinkCall):
        (JSC::JITStubs::cti_op_get_by_val):
        (JSC::JITStubs::cti_op_get_by_val_byte_array):
        (JSC::JITStubs::cti_op_put_by_val):
        (JSC::JITStubs::cti_op_put_by_val_array):
        (JSC::JITStubs::cti_op_put_by_val_byte_array):
        (JSC::JITStubs::cti_op_is_string):
        * jit/JITStubs.h:
        (JSC::JITStubs::ctiArrayLengthTrampoline):
        (JSC::JITStubs::ctiStringLengthTrampoline):
        (JSC::JITStubs::ctiVirtualCallPreLink):
        (JSC::JITStubs::ctiVirtualCallLink):
        (JSC::JITStubs::ctiVirtualCall):
        * runtime/ArrayPrototype.cpp:
        (JSC::arrayProtoFuncPop):
        (JSC::arrayProtoFuncPush):
        * runtime/FunctionPrototype.cpp:
        (JSC::functionProtoFuncApply):
        * runtime/JSArray.h:
        (JSC::isJSArray):
        * runtime/JSByteArray.h:
        (JSC::asByteArray):
        (JSC::isJSByteArray):
        * runtime/JSCell.h:
        * runtime/JSFunction.h:
        * runtime/JSGlobalData.cpp:
        (JSC::VPtrSet::VPtrSet):
        (JSC::JSGlobalData::JSGlobalData):
        (JSC::JSGlobalData::create):
        (JSC::JSGlobalData::sharedInstance):
        * runtime/JSGlobalData.h:
        * runtime/JSString.h:
        (JSC::isJSString):
        * runtime/Operations.h:
        (JSC::jsLess):
        (JSC::jsLessEq):
        * wrec/WREC.cpp:
        (JSC::WREC::Generator::compileRegExp):



git-svn-id: bf5cd6ccde378db821296732a091cfbcf5285fbd@41168 bbb929c8-8fbe-4397-9dbb-9b2b20218538"
""".lower()
    print("is performance", is_performance(text))
    print("performance in text", re.findall(build_positive_regex(), text))


