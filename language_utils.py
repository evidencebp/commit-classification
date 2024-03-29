import re
from typing import List

regex_list : List[str]

SCHEMA_NAME = 'general'
file_scheme = '([a-zA-Z0-9_\*\.])+\.[a-zA-Z]{1,4}'

REGULAR_SUFFIX = '(?:s|ed|ing)?'
VERB_E_SUFFIX = '(?:e|es|ed|ing)'

NEAR_ENOUGH = '[\S\s]{0,40}'

#term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|-|\|)" # Adding - should be tuned
#term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|\|)"
#term_seperator = "[^abcdefghijklmnopqrstuvwxyz]"
term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|_|\|)"
#term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|/|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|_|\|)" # no ",'
#term_seperator = "(\s|\.|\?|\!|\[|\]|\(|\)|\:|^|$|\,|\'|\"|#|\$|\%|&|\*|\+|=|`|;|<|>|@|~|{|}|_|\|)" # without /

# Negation
negation_terms = ["aren't",
 'arent',
 "can't",
 'cannot',
 'cant',
 'could not',
 "couldn't",
 'couldnt',
 "didn't",
 'didnt',
 "doesn't",
 'doesnt',
 "don't",
 'dont',
 "hasn't",
 "haven't",
 "isn't",
 'isnt',
 'lack',
 "n't",
 'never',
 'no',
 'nobody',
 'none',
 'not',
 'nothing',
 "shouldn't",
 'shouldnt',
 "weren't",
 'werent',
 'without',
 "won't",
 'wont',
 "wouldn't",
 'wouldnt']

# TODO - consider adding if, maybe
modals = [#'if', 'maybe',
          'can', 'could', 'ha(?:ve|s|d)', 'may', 'might', 'must', 'need', 'ought', 'shall'
    , 'should', 'will', 'would']



documentation_entities = [
    'change(?:s)?(?: |-)?(list|log|set|file)',
    'comment(s)?',
    'copy(?: |-)?right(?:s)?',
    'doc(?:s)?',
    'documentation',
    'explanation(?:s)?',
    'man(?: |-)?page(?:s)?',
    'manual',
    'note(?:s)?',
    'readme(?:.md)?',
    r'[-a-z\d_/\\]*.(md|txt)',
    'translation(?:s)?',
    'java(?: |-)?doc(?:s)?',
    'java(?: |-)?documentation',
    'example(?:s)?',
    'diagram(?:s)?',
    'guide(?:s)?',
    'gitignore',
    'icon(?:s)?',
    'doc(?: |-)?string(?:s)?',
    'tutorials(?:s)?',
    'help',
    'man',
    'doc(?: |-)?string(?:s)?',
    'desc(?:ription)?(?:s)?',
    'copy(?: |-)?right(?:s)?',
    'explanation(?:s)?',
    'release notes',
    'tag(?:s)?', # Git commit tags

]

prefective_entities = documentation_entities +[
    'indentation(?:s)?'
    , 'style'
    , 'todo(s)?'
    , 'typo(s)?'
    , 'verbosity']

software_goals = ['abstraction', 'coherence', 'cohesion', 'complexity', 'correctness', 'coupling', 'dependability'
    , 'duplication', 'efficiency', 'extensibility', 'flexibility' ,'maintainability', 'naming', 'performance', 'portability', 'quality'
    , 'readability', 'reliability', 're(?:-| )?use' ,'re(?:-| )?usability', 'security', 'simplicity', 'testability', 'testable', 're(?:-| )?usable'
    , 'readable', 'portable', 'maintainable', 'flexible', 'efficient', 'encapsulation'
                  ]

software_goals_modification = [
    'better','improv(?:e|es|ed|ing)', 'increas(?:e|es|ed|ing)', 'reduc(?:e|es|ed|ing)', 'worse', 'make', 'more', 'less'
]

software_entities = ['algorithm(?:s)?',
 'class(?:es)?',
 'collection(?:s)?',
 'constant(?:s)?',
 'constructor(?:s)?',
 'field(?:s)?',
 'function(?:s)?',
 'interface(?:s)?',
 'member(?:s)?',
 'method(?:s)?',
 'module(?:s)?',
 'parameter(?:s)?',
 'procedure(?:s)?',
 'routine(?:s)?`',
 'structure(?:s)?',
 'template(?:s)?',
 'type(?:s)?',
 'unit(?:s)?',
]

software_terms = [ 'assertion(?:s)?', 'assignment(?:s)?',  'code',  'conditional(?:s)?',  'control', 'definition(?:s)?'
    , 'delegate', 'delegation'
    , 'design pattern(?:s)?', 'error(?:-| )?code(?:s)?', 'exception(?:s)?',  'flag(?:s)?',  'getter(?:s)?'
    , 'guard clause(?:s)?', 'hierarch(?:y|ies)', 'implementation(?:s)?', 'inheritance', 'inline'
    ,  'internal', 'macro(?:s)?'
    , 'magic number(?:s)?', 'modifier(?:s)?', 'null object(?:s)?', 'object(?:s)?'
    , 'patch(?:es)?',  'pointer(?:s)?', 'polymorphism', 'quer(?:y|ies)',  'reference(?:s)?'
    , 'ref(?:s)?'
    , 'return type', 'setter(?:s)?', 'static',  'sub(?:-| )?class(?:es)?', 'super(?:-| )?class(?:es)?'
    , '(?:sub)?(?:-| )?system(?:s)?'
    , 'uninline'
    #, 'value(?:s)?'
    , 'variable(?:s)?', 'handler', 'plugin'
    #, '(?:in)?validation'
    #, 'input', 'output'
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
    , 'storage', 'tool(?:s)?',  'log(?:s)?', 'setting(?:s)?'
    #, '(?:index|indexes|indices)'
    , 'fall(?: |-)back(?:s)?', 'memory', 'param(?:s)?', 'volatile', 'file(?:s)?'
    , 'generic(?:s)?'
    #, 'test(?:s)?'
    , 'initialization(?:s)?', 'public', 'protected', 'private' ,'framework', 'singelton', 'declaration(?:s)?'
    , 'init' , 'destructor(?:s)?', 'instances(?:s)?', 'primitive(?:s)?'
    #, 'middle man'
    #, 'hierarchy'
                  ] + software_entities


# Well, we need them...
unnedded_terms = ['unnecessary', 'unneeded', 'unused', '(?:not|never|no longer) used'
    #, 'old'
    , 'no longer needed', 'redundant', 'useless', 'duplicate(?:d)?', 'deprecated', 'obsolete(?:d)?', 'commented']


static_analyzers = ['lint', 'pylint', 'tslint', 'jlint', 'jslint', 'eslint', 'klint', 'xlint', 'linter']

code_review_fixes = ['(cr|pr)(s)?(-)?(d+)?\sfix(es)?', 'fix(?:ing|es|ed)?\s(cr|pr|code review|code-review|review)']

no_message = ['no message', 'wip', 'work in progress', 'message', 'change(?:-|\s)?set', 'commit']

programming_languges = [i.lower() for i in ['Python', 'JavaScript', 'Java', 'C\+\+', 'PHP', 'TypeScript', 'C',
       'C\#', 'Go', 'Ruby', 'HTML', 'Shell', 'CSS', 'Kotlin', 'Scala',
       'Swift', 'Jupyter Notebook', 'Rust', 'Perl', 'Lua', 'Haskell', 'R',
       'Objective\-C', 'Groovy', 'Vue', 'PowerShell', 'TSQL', 'Dart',
       'Clojure', 'MATLAB', 'Emacs Lisp', 'OCaml', 'Erlang', 'Elixir',
       'CoffeeScript', 'TeX', 'Fortran', 'Assembly', 'Vim script',
       'PLpgSQL', 'Makefile', 'Julia', 'BitBake', 'F\#', 'Common Lisp',
       'Vala', 'Coq', 'Smalltalk', 'Scheme', 'Visual Basic .NET',
       'Puppet', 'HCL', 'Smarty', 'Dockerfile', 'XSLT', 'GLSL', 'Haxe',
       'Cuda', 'Ada', 'SQF', 'Pascal', 'PLSQL', 'Gherkin', 'Jsonnet',
       'Nix', 'Roff', 'Apex', 'QML', 'CMake', 'D', 'Perl 6',
       'Visual Basic', 'Objective\-C\+\+', 'Prolog', 'Mathematica',
       'Batchfile', 'Reason', 'Markdown', 'DM', 'Elm', 'FreeMarker',
       'ABAP', 'M4', 'SystemVerilog', 'AutoHotkey', 'Verilog', 'IDL',
       'Tcl', 'Rich Text Format', 'SaltStack', 'UnrealScript', 'Zig',
       'WebAssembly', 'RAML', 'F\*', 'Stan', 'ColdFusion', 'Factor',
       'LLVM', 'Pike', 'VBA', 'Isabelle', 'OpenSCAD', 'ASP', 'Arc',
       'Racket', 'LookML', 'SMT', 'q', 'Xojo', 'ZenScript', 'Ceylon',
       'Agda', 'Limbo', 'SuperCollider', 'Pawn', 'xBase', 'JSON', 'Nim',
       'M', 'XC', 'SourcePawn', 'GDScript', 'LilyPond', 'SQLPL',
       'PostScript', "Ren'Py", 'Gnuplot', 'OpenEdge ABL',
       'Common Workflow Language', 'Xtend', 'Mercury', 'Genshi',
       'Open Policy Agent', 'RobotFramework']]


def build_separated_terms(term_list : List, just_before =False):
    if just_before:
        sep = "%s(%s)" % (term_seperator, "|".join(term_list))
    else:
        sep = "%s(%s)%s" % (term_seperator, "|".join(term_list), term_seperator)
    return sep


def build_non_positive_linguistic(positive_re
                                  , neg=negation_terms):

    non_actionable_context = ['for(?:get|gets|got|getting)'
        , 'allow(s|ed|ing)?']


    return '(?:%s)' % "|".join([
        ('(?:%s)' + NEAR_ENOUGH + '(?:%s)') % (build_separated_terms(modals, just_before=True)
                                      ,  positive_re)
        , ('(?:%s)' + NEAR_ENOUGH + '(?:%s)') % (build_separated_terms(neg, just_before=True)
                                        ,  positive_re)
        , ('(?:%s)' + NEAR_ENOUGH + '(?:%s)') % (build_separated_terms(non_actionable_context, just_before=True)
                                        ,  positive_re)
        # TODO - take care of documentation entities spereatly
        #, '(?:%s)[\s\S]{0,10}(?:%s)' % (build_separated_terms(documentation_entities, just_before=True)
        #                                ,positive_re)
    ])


def match(commit_text, regex):
    text = commit_text.lower()

    return len(re.findall(regex, text))


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


def generate_bq_function(func_name
                         , code_generator
                         , commit: str ='XXX'):
    print("# Run in Standard sql ")
    print("CREATE OR REPLACE FUNCTION ")
    print(func_name)
    print(" (message string) ")
    print(" RETURNS int64 ")
    print("AS (")
    print("# Model language based on commit: {commit} ".format(commit=commit))
    code_generator()
    print(" ) ")
    print(" ; ")


def normalize(string):
    string = re.sub(r"\s+", " ", string.strip())
    while "  " in string:
        string = string.replace("  ", " ")
    return string

def print_logic_to_bq(regex_func
                      , concept):
    print("# " + concept)
    print( regex_to_big_query(regex_func()))
    print("# " + concept + " - end")
