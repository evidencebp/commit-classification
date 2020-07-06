"""
This file contain a python implementation of the corrective commit linguistic model
and the English linguistic model.
While the model used in the research was implementer in a BigQuery implementation,
the python implementation is valuable.
First, it enable to structure the model and export it for BigQuery.
Other than that, it enable running the model on test and other examples.
Running it on the train set iteratively enabled rapid evaluation of the model.

BigQuery uses the re2 engine for regular expressions, since it is fast.
This prevented us from using lookaheads and lookbehinds, which are not supported.



"""

import re

# TODO - use split to find related tokens
#  https://stackoverflow.com/questions/27060396/bigquery-split-returns-only-one-value/27158310

SCHEMA_NAME = 'general'

# Positive
bug_terms = ['(choose|take|set|use)\\s*(the|a)?\\s*correct', # correct as adjective
             "(not|isn't|doesn't)\\s+work(s|ing)?", # TODO - check with negation
             "doesn't recognize", # TODO Extend
             "caused a regression", # TODO Extend
             'bad initialization(?:s)?',
             'buffer overflow(?:s)?',
             'bug(s|z)?',
             'bug(?:-| )?fix(es)?',
             '(break|broke|breaking|broken)[\s\S]{0,20}(code|system|function|method)',
             'crash(?:ing|s|ed)?',
             'correct(?:ing|s|ed)?\\s*(a|the|some|few|this)', # make sure that correct serves as a verb
             'correct(ed|ion|ly|s)?',
             'dangling pointer(?:s)?',
             'deadlock(?:s)?',
             'defect(?:s)?',
             'double(?:-| )free',
             'error(?:s)?',
             'fail(?:ing|s|ed)?',
             'failur(?:ing|e|es|ed)',
             'fault(s)?',
             'faulty initialization(?:s)?',
             'fix(ed|es|ing)?',
             'fix(?:-| )?in(?:s)?',
             'fixing(?:s)?',
             'fix(?:-| )?up(?:s)?',
             'flaw(?:s|ed)?',
             #'hang',
             'heap overflow(?:s)?',
             'incorrect(ly)?',
             '(?:im|im-)?proper'
             'memory(?:-| )?leak(?:s)?',
             'missing\s(default value|initialization|switch case)(?:s)?',
             'add(?:ing|s|ed)?\smiss(?:ing|es|ed)?',
             'mistake(s|n|nly)?',
             #'must not',
             'null pointer(?:s)?',
             'over(?:-| )?run(?:s)?',
             'patch(?:ed|ing)',
             'problem(?:s)?',
             'race condition(?:s)?',
             'data race(?:s)?',
             'repair(?:ing|s|ed)?',
             'resource leak(?:s)?',
             # TODO - check generalization to leaks works in the other direction to expected (reduces FP, increases FN)
             'leak(?:s)?',
             'revert(?:ing|s|ed)?',
             'segmentation fault(?:s)?',
             'resolv(?:ing|e|es|ed)',
             #'solv(?:ing|e|es|ed)',
             'workaround(?:s)?',
             'wrong(nly)?',
             'trouble(?:s)?',
             'vulnerabilit(?:y|ies)']
# TODO - check https://arxiv.org/pdf/2001.09148.pdf for more
security_terms = [ 'vulnerabilit(?:y|ies)', 'cve(-d+)?(-d+)?', 'security', 'cyber', 'threat']

documentation_entities = [
    'change(?: |-)?log',
    'comment(s)?',
    'copy(?: |-)?right(?:s)?',
    'doc(?:s)?',
    'documentation',
    'explanation(?:s)?',
    'man(?: |-)?page(?:s)?',
    'manual',
    'note(?:s)?',
    'readme(?:.md)?',
    'translation(?:s)?',
    'java(?: |-)?doc(?:s)?',
    'java(?: |-)?documentation',
    'example(?:s)?',
    'diagram(?:s)?',
    'guide(?:s)?',
    'icon(?:s)?',
    'doc(?: |-)?string(?:s)?',
    'tutorials(?:s)?',
    'help',
    'man',
    'doc(?: |-)?string(?:s)?',
    'desc(?:ription)?(?:s)?',
    'copy(?: |-)?right(?:s)?',
    'explanation(?:s)?',
    'release notes'

]

prefective_entities = documentation_entities +[
    'indentation(?:s)?'
    , 'style'
    , 'todo(s)?'
    , 'typo(s)?'
    , 'verbosity']


# Valid_fix_objects
valid_fix_object = prefective_entities + ['#',
                    '(camel|snake|kebab|flat|lower|upper)\\s*case',
                    "code review('s|s)?",
                    'comment(?:s)?',
                    'cosmetic(?:s)?',
                    'cr(s)?(-)?',
                    'documentation(?:s)?',
                    'format(s|ing)?',
                    'help',
                    'remark(s)?',
                    'space(s)?',
                    'style|styling',
                    'typo(s)?',
                    'typing(?: |-)?(error|mistake)(s)?',
                    'warning(s)?',
                    'white(?: |-)?space(s)?']

valid_terms = [
    'error(?: |-)?check(ing)?',
    'error(?: |-)?handling',
    'error message(s)?',
    'error report(s|ing)?',
    'exception(?: |-)?handling',
    'fixed(?: |-)?point',
    'fix(?:ed) ticket(?:s)?',
    '(?:fix(?:ed)?|bug)(?: )?(?: |-|:)(?: )?\d+',
    '(if|would)[\s\S]{0,40}go wrong'
]

# TODO - negation changed
# Negation
negation_terms = ["aren't", "didn't" ,"don't", "doesn't", "isn't", 'lack', "n't", 'never', 'no', 'nobody', 'none', 'not'
    , 'nothing', "weren't", 'without', "won't"]

# TODO - handle term seperator
# From original CCP
#term_seperator = "(\s|\.|\?|\!|\[|\]|\)|\:|^|$|\,|\'|\"|\n|/)"
term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|\|)"
#term_seperator = "(\s|\.|\?|\!|\[|\]|\)|\:|^|$|\,|\'|\"|\n|/|\-|/|[^a-z0-9_])"
# From Refactoring
#term_seperator = "(?:^|$|[^a-z_])"
#term_seperator = "(?:^|$|[^a-z0-9_])"
#term_seperator = "(\W)"

fixing_verbs = ['correct(?:ing|s|ed)'
                    , 'fix(ed|s|es|ing)?'
                    , 'repair(?:ing|s|ed)?'
                    ,  'revert(?:ing|s|ed)?'
                    , 'resolv(?:ing|e|es|ed)'
                ]

corrective_header_entities = fixing_verbs + [
    'miss(?:ing|es|ed)?', 'should', 'must', '(have|has) to', 'avoid', 'prevent'
    #, "(does not|doesn't) need" , "cannot", "can not"
 ] #+ [ "do not" ,"don't"]


def build_sepereted_term(term_list , just_before =False):
    if just_before:
        sep = "%s(%s)" % (term_seperator, "|".join(term_list))
    else:
        sep = "%s(%s)%s" % (term_seperator, "|".join(term_list), term_seperator)
    return sep

def build_valid_find_regex():
    fix_re = "(" + "|".join(fixing_verbs) + ")"
    prefix = term_seperator + fix_re + '[\s\S]{1,40}' + "(" + "|".join(valid_fix_object) + ")" + term_seperator

    suffix = "(" + "|".join \
        (valid_fix_object) + ")" + term_seperator + '[\s\S]{0,40}' + term_seperator + fix_re + term_seperator

    # TODO - check seperation
    #sepertion = '(?:%s|%s[\s\S]{0,40}%s)' % (term_seperator, term_seperator, term_seperator)
    #suffix = "(" + "|".join \
    #    (valid_fix_object) + ")" + sepertion + fix_re + term_seperator

    other_valid_re = "(%s)" % "|".join(valid_terms)

    return "((%s)|(%s)|(%s))" % (prefix, suffix, other_valid_re)


def build_bug_fix_regex():
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(corrective_header_entities)
                                                       , term_seperator)
   # strict_header = "^(?:%s)%s"  % ( "|".join([ "do not" ,"don't"])
   #                                                    , term_seperator)

    bug_fix_re = build_sepereted_term(bug_terms)

    return "((%s)|(%s))" % (bug_fix_re, header_regex)
    #return "((%s)|(%s)|(%s))" % (bug_fix_re, header_regex, strict_header)

def build_negeted_bug_fix_regex():
    bug_fix_re = build_bug_fix_regex()
    negation_re = build_sepereted_term(negation_terms)


    return "%s[\s\S]{0,20}%s" % (negation_re, bug_fix_re)



def is_fix(commit_text):

    text = commit_text.lower()

    fix_num = len(re.findall(build_bug_fix_regex(), text))
    valid_num = len(re.findall(build_valid_find_regex(), text))
    negated_num = len(re.findall(build_negeted_bug_fix_regex(), text))
    # TODO  consider modals
    #negated_num = len(re.findall(build_non_positive_linguistic(build_bug_fix_regex()), text))
    return (fix_num - valid_num - negated_num) > 0
    #return (fix_num ) > 0 # max recall with current predictor


software_goals = ['abstraction', 'coherence', 'cohesion', 'complexity', 'correctness', 'coupling', 'dependability'
    , 'duplication', 'efficiency', 'extensibility', 'flexibility' ,'maintainability', 'naming', 'performance', 'portability', 'quality'
    , 'readability', 'reliability', 're(?:-| )?use' ,'re(?:-| )?usability', 'security', 'simplicity', 'testability', 'testable', 're(?:-| )?usable'
    , 'readable', 'portable', 'maintainable', 'flexible', 'efficient', 'encapsulation'
                  ]

software_goals_modification = [
    'better','improv(?:e|es|ed|ing)', 'increas(?:e|es|ed|ing)', 'reduc(?:e|es|ed|ing)', 'worse', 'make', 'more', 'less'
]

software_terms = ['algorithm(?:s)?', 'assertion(?:s)?', 'assignment(?:s)?', 'class(?:es)?', 'code', 'collection(?:s)?'
    , 'conditional(?:s)?', 'constant(?:s)?', 'constructor(?:s)?', 'control', 'definition(?:s)?'
    , 'delegate', 'delegation'
    , 'design pattern(?:s)?', 'error(?:-| )?code(?:s)?', 'exception(?:s)?', 'field(?:s)?', 'flag(?:s)?', 'function(?:s)?', 'getter(?:s)?'
    , 'guard clause(?:s)?', 'hierarch(?:y|ies)', 'implementation(?:s)?', 'inheritance', 'inline'
    , 'interface(?:s)?', 'internal', 'macro(?:s)?'
    , 'magic number(?:s)?', 'member(?:s)?', 'method(?:s)?', 'modifier(?:s)?', 'null object(?:s)?', 'object(?:s)?', 'parameter(?:s)?'
    , 'patch(?:es)?',  'pointer(?:s)?', 'polymorphism', 'quer(?:y|ies)',  'reference(?:s)?'
    , 'ref(?:s)?'
    , 'return type', 'setter(?:s)?', 'static', 'structure(?:s)?', 'sub(?:-| )?class(?:es)?', 'super(?:-| )?class(?:es)?', '(?:sub)?(?:-| )?system(?:s)?'
    , 'template(?:s)?', 'type(?:s)?'
    , 'uninline'
    #, 'value(?:s)?'
    , 'variable(?:s)?', 'handler', 'plugin'
    #, '(?:in)?validation'
    #, 'input', 'output'
    , 'unit(?:s)?'
    , 'contravariant', 'covariant'
                  # , 'link(?:s)?'
    ,
                  'action(?:s)?'
                  # , 'event(?:s)?'
    , 'queue(?:s)?', 'stack(?:s)?'
    #, 'change(?:\s)?log'
    , 'driver(?:s)?'
    #, 'hook(?:s)?'
    #, 'target(?:s)?'
    , 'storage', 'tool(?:s)?', 'module(?:s)?', 'log(?:s)?', 'setting(?:s)?'
    #, '(?:index|indexes|indices)'
    , 'fall(?: |-)back(?:s)?', 'memory', 'param(?:s)?', 'volatile', 'file(?:s)?'
    , 'generic(?:s)?'
    #, 'test(?:s)?'
    , 'initialization(?:s)?', 'public', 'protected', 'private' ,'framework', 'singelton', 'declaration(?:s)?'
    , 'init' , 'destructor(?:s)?', 'instances(?:s)?', 'primitive(?:s)?'
    #, 'middle man'
    #, 'hierarchy'
                  ]

# TODO - add Technical Debt, fixme
# https://arxiv.org/pdf/2002.11049.pdf
refactor_entities = software_terms + ['(helper|utility|auxiliary) function(?:s)?']


# Well, we need them...
unnedded_terms = ['unnecessary', 'unneeded', 'unused', '(?:not|never|no longer) used'
    #, 'old'
    , 'no longer needed', 'redundant', 'useless', 'duplicate(?:d)?', 'deprecated', 'obsolete(?:d)?', 'commented']


modification_activity = [
                            #'chang(?:e|esed|ing)'
 'clean(?:ing|s|ed)?'
#,
                            'clean(?:ing)?(?:-| )?up(?:s)?'
    , 'combin(?:e|es|ed|ing)',
           'compos(?:e|es|ed|ing)','de(?:-| )?compos(?:e|es|ed|ing)', 'convert(?:ed|s|ing)?'
                            #, 'creat(?:e|es|ed|ing)'
                            , 'dead'
#, 'delet(?:e|es|ed|ing)'
                            , 'deprecat(?:e|es|ed|ing)'
                            , 'drop(?:ed|s|ing)?', 'duplicat(?:e|es|ed|ing)', 'extract(?:ed|s|ing)?'
           # Goals modification only?
                            ,'improv(?:e|es|ed|ing)', 'increas(?:e|es|ed|ing)'
                            #, 'instead'
                            #, 'kill(?:ed|s|ing)?'
                            , '(?:make|makes|made|making)'
                            , 'mov(?:e|es|ed|ing)'
           # , 'provid(?:e|es|ed|ing)'
                            , 'rebuil(?:d|ds|ding|t)'
                            , 'replac(?:e|es|ed|ing)', 'redundant', 're(?:-|)?organiz(?:e|es|ed|ing)'
    , 're(?:-|)?structur(?:e|es|ed|ing)','separat(?:e|e s|ed|ing)'
                            , 'split(?:s|ing)?', 'subsitut(?:e|es|ed|ing)', 'tid(?:y|ying|ied)'
, 'short(:?en|er|ing|s)?', 'polish(?:ed|es|ing)?', '(?:get|got|getting) rid', 'encapsulate'
                            , 'hide(?:e|es|ed|ing)', 'un(?:-| )?hid(?:e|es|ed|ing)'
                            , 'parameteriz(?:e|es|ed|ing)'
                            , 'substitut(?:e|es|ed|ing)'
                            #, 'introduc(?:e|es|ed|ing)'
                        , ] + unnedded_terms

feedbak_terms = [ 'py(?:-| )?lint', 'lint', 'review comments(?:s)?', 'code review', 'cr', 'pep8'
                  ]
feedback_action = ['fix(?:ed|s|es|ing)?', 'fix(?:-| )?up(?:s)?', 'resolv(?:e|ed|es|ing)', 'correct(?:ed|s|es|ing)?']

perfective_header_action = [
    #'polish(?:ed|es|ing)?'
    #, 'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
     'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
    , 'cleaner'
    , 'deprecat(?:e|es|ed|ing)'
    , 'extract(?:ed|s|ing)?',
    're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)', 'tid(?:y|ying|ied) up'
    , 'improv(?:e|ed|es|ing|ement|ements)' , 're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)'
    , '(helper|utility|auxiliary) function(?:s)?'
    , '(?:move|moved|moves|moving) to'
    , 'separat(?:e|es|ed|ing)'
    , 'split(?:s|ing)?', '->'
    #, '(private|public|protected|static)'
]

# TODO - rewrited, move into/out???, deduplicate, remove legacy, redo, PR, feedback

# TODO - clean , style, prettier, "->", refine, "Removed commented code", "More startup improvements.", recode
# ""Remove another old function", "improved redis error message", utility functions, never used
# Checkstyle


# TODO - perfective, not refactor - ident, spacing, tabs, "tabs -> spaces", cosmetic, ""*** empty log message ***"
# examples ""DOC: remove mention of TimeSeries in docs"

# TODO - add "resolving review comments"
# TODO - lint, pylint
refactor_context = [ 'clean(ing)?(-| )?up(s)?'
    ,'call(?:s|ed|ing)?[\s\S]{1,50}instead'
    , 'collaps(?:e|es|ed|ing)', 'consolidat(e|es|ed|ing)'
    , 'decompos(?:e|es|ed|ing)'
    , 'drop(?:ed|s|ing)?( back)', 'encapsulat(e|es|ed|ing)'
    , 'gereneliz(?:e|es|ed|ing)'
                    # , 'inline'
                    # , 'no longer needed', 'not used', 'obsolete(d)?'
    , 'optimiz(?:e|es|ed|ing|ation|ations)'
    , 'pull(?:ed|s|ing)? (up|down)', 're(?:-)?(?:write|wrote)', 're(?:-| )?factor(?:ed|s|ing|ings)?'
    , 're(-)?implement(ed|s|ing)?'
    , 'renam(?:e|es|ed|ing|ings)', 'better nam(?:e|es|ing)','re(?:-)?organiz(e|es|ed|ing)', 're(?:-)?organization'
    , 're(?:-)?work(ed|s|ing|ings)?'
    , 'reorg' , 'simplif(y|es|ied|ying|ication)', 'suppress(es|ed|ing)? warning(?:s)?'
    , 'unif(?:y|ies|ied|ing)', 'uninline'
    , 'beef(?:ed|s|ing)? up', 'refactor(?:ing)?(?:s)?', 'code improvement(?:s)?'
    #, '(?:^|^[\s\S]{0,25}%s)(?:%s)%s[\s\S]{0,25}$' % (term_seperator, "|".join(perfective_header_action), term_seperator)
    , 'revis(?:e|es|ed|ing)'
    , 're(?:-)?construct(?:s|ed|ing)?'
    , 're(?:-)?(?:write|write|wrote|writing)'
    , 're(?:-)?cod(?:e|ed|es|ing)'
    , 'factor(?:ed|s|ing)? out'
    , 're(?:-| )?packag(?:e|es|ed|ing)'
    #, 'code review'
    #, 'collapse'
    #, "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(feedback_action
    #                                                                                      , just_before=True)
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , "|".join(feedbak_terms)
    #                                                                 , term_seperator)
                    # ,'us(e|es|ed|ing)[\s\S]{1,50}(instead)'
                    # , '(instead)[\s\S]{1,50}us(e|es|ed|ing)'
                    ]
# https://refactoring.guru/refactoring/techniques

# TODO - change [\s\S] with . ?
removal = [ 'add(?:s|ed|ing)?[\s\S]{1,50}helper(?:s)?'
    ,  'us(?:e|es|ed|ing)[\s\S]{1,50}instead'
    #,  'us(?:e|es|ed|ing)[\s\S]{1,25}\(\)[\s\S]{1,25}instead'
    ,  'split(?:s|ing)?[\s\S]{1,50}into'
    ,  'break(?:s|ing)?[\s\S]{1,50}into'
    ,  'separat(?:e|e s|ed|ing)[\s\S]{1,50}into'
    #,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}with'
    ,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    , 'remov(?:e|es|ed|ing)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    #, '(?:this|that|is)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'kill(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'drop(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'mov(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
            ]
adaptive_context = [
    '(?:un)?hid(?:e|es|den)', 'add(?:s|ed|ing)?', 'allow(?:s|ed|ing)?'
    , 'buil(?:t|ds|ing)', 'calibirat(?:e|es|ed|ing)'
    , 'configure'
    , 'creat(?:e|es|ing)' #   O created
    , 'deferr(?:ed|s|ing)?'
    , 'disabl(?:e|es|ed|ing)'
    , 'enhanc(?:e|es|ed|ing)', 'extend(?:s|ed|ing)?', 'form(?:ed|s|ing)?'
    , 'implement(?:ed|s|ing)?', 'import(?:s|ed|ing)?', 'introduc(?:e|es|ed|ing)'
    , 'port(?:s|ed|ing)?'
    , 'provid(?:e|es|ed|ing)'
    , 'report(?:s|ed|ing)?'
    , 'support(s|ed|ing)?'
    , 'updat(?:e|es|ed|ing)'
    , 'upgrad(?:e|es|ed|ing)'

    # , 'mov(e|es|ed|ing)'
    # , 'print(s|ed|ing)?'


]


#

# 'build', , 'mark(s|ed|ing)?', 'mov(e|es|ed|ing)', 'us(e|es|ed|ing)'
adaptive_context_old = [
    'allow(?:s|ed|ing)?'
    , 'add(?:s|ed|ing)?'
    ,' build'
    # , 'mark(s|ed|ing)?', 'mov(e|es|ed|ing)', 'us(e|es|ed|ing)'
    ,' (?:make|makes|made|making)'
    ,' (?:un)?hid(e|es|den)'
    , 'allow(?:s|ed|ing)?'
    , 'buil(?:t|ds|ing)'
    , 'calibirat(?:e|es|ed|ing)'
    , 'chang(?:e|es|ed|ing)'
    , 'complet(?:e|es|ed|ing)'
    , 'configure'
    # , 'creat(e|es|ed|ing)'
    , 'creat(?:e|es|ing)'  # NO created
    , 'deferr(?:ed|s|ing)?'
    , 'disabl(?:e|es|ed|ing)'
    , 'enabl(?:e|es|ed|ing)'
    , 'enhanc(?:e|es|ed|ing)', 'extend(?:s|ed|ing)?', 'form(?:ed|s|ing)?'
    , '(get|got|getting)'
    # , 'handl(e|es|ed|ing)'
    , '\simplement(ed|s|ing)?'
    , 'import(s|ed|ing)?', 'introduc(e|es|ed|ing)'
    , 'new'
    , 'port(s|ed|ing)?'
    , 'preserv(?:e|es|ing)'
    , 'print(s|ed|ing)?'
    , 'provid(e|es|ed|ing)'
    , 'quirk(s|ed|ing)?'
    , '(rm|remov(e|es|ed|ing))'
    , 'report(s|ed|ing)?'
    , 're(-)?buil(d|ds|t|ding)'
    , 're(-)?calibirat(e|es|ed|ing)'
    , '(set|sets|setting)'
    , 'switch(es|ed|ing)?'
    , 'support(s|ed|ing)?'
    # , 'us(e|es|ed|ing)'
    , 'updat(e|es|ed|ing)'
    , 'upgrad(e|es|ed|ing)'
]

adaptive_entities = ['ability', 'configuration', 'conversion', 'debug', 'new', 'possibility', 'support'
    , 'test(s)?', 'tweak(s)?', 'mode', 'option']


def match(commit_text, regex):
    text = commit_text.lower()

    return len(re.findall(regex, text))



def build_refactor_regex():
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , term_seperator)

    activity_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(modification_activity
                                                                                          , just_before=True)
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , "|".join(refactor_entities)
                                                                     , term_seperator)
    return "(%s)|(%s)|(%s)" % (build_sepereted_term(refactor_context)
                          , activity_regerx
                          , header_regex)


def build_refactor_goals_regex():
    goals_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(software_goals_modification
                                                                                       , just_before=True)
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , "|".join(software_goals)
                                                                  , term_seperator)
    return goals_regerx


def build_non_code_perfective_regex():

    non_perfective_entities = ['warning(?:s)?'
                               , 'format(?:ting)?'
                               , 'indentation(?:s)?'
                              ]
    # TODO - applied to perfective entities too here, which is a bug.
    modification_action = ['clean(?:-| )?up(?:s)?']
    non_perfective_context = [
                            'fix(?:es|ed|ing)?'
                            ,'(?:get|got|getting) rid'
                            , 'support(?:s|ed|ing)?'
                            ]
    modifiers = modification_activity + non_perfective_context
    activity_regerx = "((?:%s)(?:\s|%s[\s\S]{0,50}%s)(?:%s))" % (build_sepereted_term(modifiers, just_before=True)
                                                                                , term_seperator
                                                                                , term_seperator
                                                                                , "|".join(prefective_entities
                                                                                           + non_perfective_entities))
    doc_header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)[\s\S]{0,25}(?:%s)' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , build_sepereted_term(documentation_entities))


    no_prefective_action = "|".join([
        'convert(?:ed|s|ing)?(?:%s|%s[\s\S]{0,50}%s)support(?:s|ed|ing)?' % (
            term_seperator,term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)work' % (term_seperator, term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)sense' % (term_seperator, term_seperator, term_seperator)
        , 'improv(?:e|es|ed|ing) handling'
        , '(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)' %(build_sepereted_term(non_perfective_entities,just_before=True)
                                                   ,term_seperator
                                                   , term_seperator
                                                   , term_seperator
                                                   , "|".join(modification_action)
                                                   )
        , doc_header_regex

    ])
    non_perfective_context = '(?:%s|%s)' % (no_prefective_action
                                         , activity_regerx)

    return non_perfective_context


# instead of
# make sure
# missed to create
# can be replaced, e9dee4fc76caaca231bf10728d4f82bc46581bc5
# no seperation for create eb1027b5e8c047059f68e7547188d08c7fde0b6f
# inline c9d4924dcf129512dadd22dcd6fe0046cbcded43
# can be optimized 197fc962fa8a3153dc058abfa2ae8c816d67ea04
# corrective trouble (use wordnet) b580f0706dc1dcded6d1a584c37a83dd1cb2ea2a
# not used 72894b26c24b1ea31c6dda4634cfde67e7dc3050


def built_is_refactor(commit_text):
    removal_re = build_sepereted_term(removal)

    return (match(commit_text, build_refactor_regex())
            + match(commit_text, removal_re)
            + match(commit_text, build_refactor_goals_regex())
            - match(commit_text, build_non_code_perfective_regex())
            - match(commit_text, build_documentation_entities_context(build_refactor_regex()))
            - match(commit_text, build_non_positive_linguistic(build_refactor_regex()))
            - match(commit_text, build_non_positive_linguistic(build_sepereted_term(removal)))
            - match(commit_text, build_non_positive_linguistic(build_refactor_goals_regex()))
            ) > 0

def build_perfective_regex():
    non_code = build_sepereted_term (prefective_entities)

    perfective = "(%s)" %  non_code

    return perfective

adaptive_header_action = "|".join([
    'upgrad(?:e|es|ed|ing)',
    'configur(?:e|es|ed|ing)',
    '(?:keep|change)\s+(?:the\s+)?default',
    'new',
    # 'merg(?:e|es|ed|ing)',
    # '(?:make(?:s)?|made|making)',
    # 'merg(?:e|es|ed|ing)',
    'clear(?:s|ed|ing)?',
    # 'convert(?:s|ed|ing)?',
    # 'check(?:s|ed|ing)?',
    'add(?:s|ed|ing)?',
    # 'build',
    # 'buil(?:d|t|ds|ing)',
    '(?:im)?port(?:s|ed|ing)?',
    '(?:un)?hid(?:e|es|den)',
    'updat(?:e|es|ed|ing)',
    'disabl(?:e|es|ed|ing)',
    'enabl(?:e|es|ed|ing)',
    'quirk(?:s|ed|ing)?',
    'allow(?:s|ed|ing)?',
    'provid(e|es|ed|ing)',
    # 'remov(e|es|ed|ing)'

    ###
    # , 'build'
    # , 'mark(?:s|ed|ing)?'
    # , 'us(?:e|es|ed|ing)'
    # , '(?:make|made|making)'
    # , 'chang(?:e|es|ed|ing)'
    # , 'creat(?:e|es|ed|ing)'
    # , 'enabl(?:e|es|ed|ing)'
    # , 'handl(?:e|es|ed|ing)'
    'remov(?:e|es|ed|ing)'

])

file_scheme = '([a-z  -Z0-9_\*\.])+\.[a-zA-Z]{1,4}'

adaptive_actions = [  # 'revert(?:s|ed|ing)?',
    #'merg(?:e|es|ed|ing)[\s\S]{1,5}(pull request|pr|branch)',
    'add(?:s|ed|ing)?[\s\S]{1,50}(?:version|v\d|ver\d)',
    '(^|\s)implement(?:ed|s|ing)?\s',
    '(?:make(?:s)?|made|making)[\s\S]{1,50}consitent',
    'updat(?:e|es|ed|ing)[\s\S]{1,25}to[\s\S]{1,25}\d+.\d',
    'updat(?:e|es|ed|ing)\s+(to\s+)?\d+\.\d',
    '(?:add(s|ed|ing)?|delet(?:e|es|ed|ing)|updat(?:e|es|ed|ing))\s+' + file_scheme,
    # '(add(s|ed|ing)?|delet(e|es|ed|ing)|updat(e|es|ed|ing))\s+([A-Z0-9_]*)', # TODO - run without lower
    '(^|^[\s\S]{0,25}%s)(%s)%s' % (term_seperator, adaptive_header_action, term_seperator),
    # '^(?:version|v\d+\.\d|ver\d+\.\d)',
    '^\[(?:IMP|imp)\]',  # TODO - take care of upper/lower case
    'support(?:s|ed|ing)?\sfor\s',
    'show(?:es|ed|ing)?[\s\S]instead']


def build_adaptive_action_regex():

    return "(%s)" % ("|".join(
    adaptive_actions))




def build_adaptive_regex():

    adaptive_context_re = build_sepereted_term(adaptive_context, just_before=True)


    return "((%s)\s[\s\S]{0,50}(%s)%s)" % (adaptive_context_re
                            ,  "|".join(adaptive_entities + software_terms)
                            , term_seperator)


modals = ['can', 'could', 'ha(?:ve|s|d)', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']

def build_non_adaptive_context():

    non_adaptive_header_action = "|".join([
                                'transla(?:tion|et|eted|ets|ting)'
                                ,  'readme(?:.md)?'
                              ])

    non_adaptive_header ='^[\s\S]{0,50}(%s)' % non_adaptive_header_action

    entities = documentation_entities + ['bug',
                'helper',
                'miss(?:ing|ed)',
                'to(?: |-)?do(?:s)?',
                'warning(?:s)?'
                ]

    adaptive_actions = ['remov(?:e|es|ed|ing)']
    non_adaptive_entities = documentation_entities + software_terms + unnedded_terms + [file_scheme]


    return '(%s)' % "|".join(['(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_context, just_before=True)
                                                            , "|".join(entities))
                     , non_adaptive_header
                     , '(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_actions, just_before=True)
                                                            , "|".join(non_adaptive_entities))
                     ])





def build_non_positive_linguistic(positive_re):

    non_actionable_context = ['for(?:get|gets|got|geting)'
        , 'allow(s|ed|ing)?']


    return '(?:%s)' % "|".join([
        '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(modals, just_before=True)
                                      ,  positive_re)
        , '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(negation_terms, just_before=True)
                                        ,  positive_re)
        , '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(non_actionable_context, just_before=True)
                                        ,  positive_re)
        # TODO - take care of documentation entities spereatly
        #, '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(documentation_entities, just_before=True)
        #                                ,positive_re)
    ])

def build_documentation_entities_context(positive_re):

    return '(?:%s)' % "|".join([
        # TODO - take care of documentation entities spereatly
         '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(documentation_entities, just_before=True)
                                        ,positive_re)
    ])



def build_non_adaptive_linguistic():

    return build_non_positive_linguistic(build_adaptive_regex())

def is_adaptive(text):

    return (match(text, build_adaptive_regex())
            + match(text, build_adaptive_action_regex())
            - match(text, build_non_adaptive_context())
            - match(text, build_non_adaptive_linguistic()))

def classifiy_commits_df(df):
    df['corrective_pred'] = df.message.map(lambda x: is_fix(x))
    df['is_refactor_pred'] = df.message.map(lambda x: built_is_refactor(x))
    df['perfective_pred'] = df.message.map(lambda x: (match(x, build_perfective_regex())) +
                                                     (match(x, build_refactor_regex())) > 0)
    df['adaptive_pred'] = df.message.map(lambda x: is_adaptive(x) > 0)

    return df


def regex_to_big_query(reg_exp
                       , text_field='message'):
    # TODO - check
    # Take care of encoding
    reg_exp = reg_exp.replace("\\", "\\\\").replace("'", "\\'")
    #reg_exp = reg_exp.replace("\\\\", "\\")
    # No need for grouping
    reg_exp = reg_exp.replace("(?:", "(")
    str = "(" + "LENGTH(REGEXP_REPLACE(lower(" + text_field + ")," + "'%s', '@'))" % reg_exp + "-" \
          + "LENGTH(REGEXP_REPLACE(lower(" + text_field + ")," + "'%s', ''))" % reg_exp + ")"

    return str

def corrective_to_bq():
    # TODO - the \n in the string seperator is printed as a new line and should be fixed
    print("# Corrective")
    print( "# Corrective : build_bug_fix_regex()")
    #print( ",")
    print( regex_to_big_query(build_bug_fix_regex()))
    print(" - ")
    print( "# Corrective : build_valid_find_regex()")
    print( regex_to_big_query(build_valid_find_regex()))
    print(" - ")
    print( "# Corrective : build_negeted_bug_fix_regex()")
    print( regex_to_big_query(build_negeted_bug_fix_regex()))
    print("#Corrective - end")

def adaptive_to_bq():


    print("# Adaptive")
    print( "# Adaptive :build_adaptive_regex()")
    #print( ",")
    print( regex_to_big_query(build_adaptive_regex()))
    print( "#Adaptive :build_adaptive_action_regex()")
    print( "+")
    print( regex_to_big_query(build_adaptive_action_regex()))
    print( "# Adaptive :build_non_adaptive_context()")
    print( "-")
    print( regex_to_big_query(build_non_adaptive_context()))
    print( "# Adaptive :build_non_adaptive_linguistic()")
    print( "-")
    print( regex_to_big_query(build_non_adaptive_linguistic()))
    print("# Adaptive - end")


def positive_refactor_to_bq():
    print( "# Refactor :build_refactor_regex()")
    #print( ",")
    print( regex_to_big_query(build_refactor_regex()))
    print( "# Refactor :build_sepereted_term(removal)")
    print( "+")
    print( regex_to_big_query(build_sepereted_term(removal)))

    print( "# Refactor :build_refactor_goals_regex()")
    print( "+")
    print( regex_to_big_query(build_refactor_goals_regex()))


def non_code_refactor_to_bq():
    print( "# Refactor :build_non_code_perfective_regex()")
    print( regex_to_big_query(build_non_code_perfective_regex()))

def non_positive_linguistic_refactor_to_bq():
    print( "# Refactor :build_non_positive_linguistic(build_refactor_regex())")
    print( "-")
    print( regex_to_big_query(build_non_positive_linguistic(build_refactor_regex())))

def non_positive_linguistic_refactor_goals_to_bq():
    print( "# Refactor :build_non_positive_linguistic(build_refactor_goals_regex())")
    print( regex_to_big_query(build_non_positive_linguistic(build_refactor_goals_regex())))

def non_positive_linguistic_removal_to_bq():
    print("# Refactor :build_non_positive_linguistic(build_sepereted_term(removal))")
    print(regex_to_big_query(build_non_positive_linguistic(build_sepereted_term(removal))))


def documentation_entities_context_refactor_to_bq():
    print("# Refactor :build_documentation_entities_context(build_refactor_regex())")
    print(regex_to_big_query( build_documentation_entities_context(build_refactor_regex())))



def refactor_to_bq():

    print( "# Refactor")

    print('{schema}.bq_positive_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_code_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor_goals(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_non_positive_linguistic_refactor_removal(message)'.format(schema=SCHEMA_NAME))
    print(' - {schema}.bq_documentation_entities_context_refactor(message)'.format(schema=SCHEMA_NAME))

    print( "# Refactor - end ")



def just_perfective_to_bq():

    print("# Just Perfective")
    print( "# Perfective :build_perfective_regex()")
    #print( ",")
    print( regex_to_big_query(build_perfective_regex()))

def perfective_to_bq():

    print( "# Perfective")

    print('{schema}.bq_just_perfective(message)'.format(schema=SCHEMA_NAME))
    print(' + {schema}.bq_refactor(message)'.format(schema=SCHEMA_NAME))

    print( "# Perfective - end ")



def generate_bq_function(func_name
                         , code_generator):
    print("# Run in Starndad sql ")
    print("CREATE OR REPLACE FUNCTION ")
    print(func_name)
    print(" (message string) ")
    print(" RETURNS int64 ")
    print("AS (")
    print("# Model language based on commit: XXX ")
    code_generator()
    print(" ) ")
    print(" ; ")

def print_bq_functions():
    print()
    generate_bq_function('{schema}.bq_corrective'.format(schema=SCHEMA_NAME), corrective_to_bq)
    print()
    generate_bq_function('{schema}.bq_adaptive'.format(schema=SCHEMA_NAME), adaptive_to_bq)
    print()


    generate_bq_function('{schema}.bq_English'.format(schema=SCHEMA_NAME), English_to_bq)
    print()


    generate_bq_function('{schema}.bq_positive_refactor'.format(schema=SCHEMA_NAME), positive_refactor_to_bq)
    print()

    generate_bq_function('{schema}.bq_non_code_refactor'.format(schema=SCHEMA_NAME), non_code_refactor_to_bq)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor'.format(schema=SCHEMA_NAME), non_positive_linguistic_refactor_to_bq)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor_goals'.format(schema=SCHEMA_NAME)
                         , non_positive_linguistic_refactor_goals_to_bq)
    print()

    generate_bq_function('{schema}.bq_non_positive_linguistic_refactor_removal'.format(schema=SCHEMA_NAME)
                         , non_positive_linguistic_removal_to_bq)
    print()


    generate_bq_function('{schema}.bq_documentation_entities_context_refactor'.format(schema=SCHEMA_NAME)
                         , documentation_entities_context_refactor_to_bq)
    print()

    generate_bq_function('{schema}.bq_refactor'.format(schema=SCHEMA_NAME), refactor_to_bq)
    print()

    generate_bq_function('{schema}.bq_just_perfective'.format(schema=SCHEMA_NAME), just_perfective_to_bq)
    print()

    generate_bq_function('{schema}.bq_perfective'.format(schema=SCHEMA_NAME), perfective_to_bq)
    print()


def English_to_bq():

    print("# English")
    print( "# English :build_English_regex()")
    #print( ",")
    print( regex_to_big_query(build_English_regex()))

English_terms = ['about', 'all', 'also', 'and', 'because', 'but', 'can', 'come', 'could', 'day', 'even', 'find'
    , 'first', 'for', 'from', 'get', 'give', 'have', 'her', 'here', 'him', 'his', 'how', 'into', 'its', 'just', 'know'
    , 'like', 'look', 'make', 'man', 'many', 'more', 'new', 'not', 'now', 'one', 'only', 'other', 'our', 'out'
    , 'people', 'say', 'see', 'she', 'some', 'take', 'tell', 'than', 'that', 'the', 'their', 'them', 'then', 'there'
    , 'these', 'they', 'thing', 'think', 'this', 'those', 'time', 'two', 'use', 'very', 'want', 'way', 'well', 'what'
    , 'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']

def build_English_regex():
    Eng_re = "%s(%s)%s" % (term_seperator
                               , "|".join(English_terms)
                               , term_seperator)

    return Eng_re

def is_English(commit_text):
    text = commit_text.lower()

    English_num = len(re.findall(build_English_regex(), text))

    return English_num > 0


if __name__ == '__main__':
    print_bq_functions()