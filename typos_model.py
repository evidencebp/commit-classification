# Based on https://en.wikipedia.org/wiki/Commonly_misspelled_English_words

# Function words
# https://www.youtube.com/watch?app=desktop&v=PGsQwAu3PzU
# https://semanticsimilarity.files.wordpress.com/2013/08/jim-oshea-clustered-fwlist-277.pdf

from os.path import join
import re

from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier


positive_terms = [
'absense' # mistake of absence
,'absentse' # mistake of absence
,'abcense' # mistake of absence
,'absance' # mistake of absence
,'acceptible' # mistake of acceptable
,'accidentaly' # mistake of accidentally/accidently
,'accomodate' # mistake of accommodate
,'acommodate' # mistake of accommodate
,'acheive' # mistake of achieve
#,'agrieve' # mistake of aggrieved - Alos a name
,'acknowlege' # mistake of acknowledge
,'aknowledge' # mistake of acknowledge
,'acquaintence' # mistake of acquaintance
,'aquaintance' # mistake of acquaintance
,'aquire' # mistake of acquire
,'adquire' # mistake of acquire
,'aquit' # mistake of acquit
,'acrage' # mistake of acreage
,'acerage' # mistake of acreage
,'adress' # mistake of address
,'adultary' # mistake of adultery
,'adviseable' # mistake of advisable
,'advizable' # mistake of advisable
#,'effect' # mistake of affect
,'agression' # mistake of aggression
,'agressive' # mistake of aggressive
,'allegaince' # mistake of allegiance
,'allegience' # mistake of allegiance
,'alegiance' # mistake of allegiance
,'allmost' # mistake of almost
,'alot' # mistake of a lot
,'amatuer' # mistake of amateur
,'amature' # mistake of amateur
,'anually' # mistake of annually
,'annualy' # mistake of annually
,'apparant' # mistake of apparent
,'aparent' # mistake of apparent
,'apparrent' # mistake of apparent
,'aparrent' # mistake of apparent
,'artic' # mistake of arctic
,'arguement' # mistake of argument
,'athiest' # mistake of atheist
,'athist' # mistake of atheist
,'awfull' # mistake of awful
,'aweful' # mistake of awful
,'becuase' # mistake of because
,'beatiful' # mistake of beautiful
,'becomeing' # mistake of becoming
,'begining' # mistake of beginning
,'beleive' # mistake of believe
,'bellweather' # mistake of bellwether
#,'bouy/bouyant' # mistake of buoy/buoyant
,'buisness' # mistake of business
,'calender' # mistake of calendar
,'camoflage' # mistake of camouflage
,'camoflague' # mistake of camouflage
#,'capital' # mistake of capitol
,'carribean' # mistake of Caribbean
,'catagory' # mistake of category
,'cauhgt' # mistake of caught
,'caugt' # mistake of caught
,'cemetary' # mistake of cemetery
,'changable' # mistake of changeable
,'cheif' # mistake of chief
,'collaegue' # mistake of colleague
,'collegue' # mistake of colleague
,'colum' # mistake of column
,'comming' # mistake of coming
,'commited' # mistake of committed
,'comitted' # mistake of committed
,'comparsion' # mistake of comparison
,'conceed' # mistake of concede
,'congradulate' # mistake of congratulate
,'consciencious' # mistake of conscientious
,'concious' # mistake of conscious
,'consious' # mistake of conscious
,'concensus' # mistake of consensus
,'contraversy' # mistake of controversy
,'cooly' # mistake of coolly
,'dacquiri' # mistake of daiquiri
,'daquiri' # mistake of daiquiri
,'decieve' # mistake of deceive
,'definate' # mistake of definite
,'definitly' # mistake of definitely
,'desparate' # mistake of desperate
,'diffrence' # mistake of difference
,'dilema' # mistake of dilemma
,'dissapoint' # mistake of disappoint
,'disasterous' # mistake of disastrous
,'drunkeness' # mistake of drunkenness
,'dumbell' # mistake of dumbbell
,'embarass' # mistake of embarrass
,'equiptment' # mistake of equipment
,'excede' # mistake of exceed
,'exilerate' # mistake of exhilarate
,'existance' # mistake of existence
,'experiance' # mistake of experience
,'extreem' # mistake of extreme
,'facinating' # mistake of fascinating
,'firey' # mistake of fiery
,'flourescent' # mistake of fluorescent
,'foriegn' # mistake of foreign
,'freind' # mistake of friend
,'fullfil' # mistake of fulfil
, 'functionnal' # mistake of functional
,'guage' # mistake of gauge
,'gratefull' # mistake of grateful
,'greatful' # mistake of grateful
,'grate' # mistake of great
,'grat' # mistake of great
,'garantee' # mistake of guarantee
,'garentee' # mistake of guarantee
,'garanty' # mistake of guarantee
,'guidence' # mistake of guidance
,'harrass' # mistake of harass
,'heighth' # mistake of height
,'heigth' # mistake of height
,'heirarchy' # mistake of hierarchy
,'hors derves' # mistake of hors d'oeuvres
,'ordeurves' # mistake of hors d'oeuvres
,'humerous' # mistake of humorous
,'hygene' # mistake of hygiene
,'hygine' # mistake of hygiene
,'hiygeine' # mistake of hygiene
,'higeine' # mistake of hygiene
,'hygeine' # mistake of hygiene
,'hipocrit' # mistake of hypocrisy/hypocrite
,'ignorence' # mistake of ignorance
,'immitate' # mistake of imitate
,'imediately' # mistake of immediately
,'indite' # mistake of indict
,'independant' # mistake of independent
,'indispensible' # mistake of indispensable
,'initialise' # mistake of initialize
,'innoculate' # mistake of inoculate
,'inteligence' # mistake of intelligence
,'intelligance' # mistake of intelligence
#,'jason' # mistake of json (JSON format), yet also the name Jason
,'jewelery' # mistake of jewelry (UK: jewellery)
,'judgement' # mistake of judgment
,'kernal' # mistake of kernel
,'liesure' # mistake of leisure
,'liason' # mistake of liaison
,'libary' # mistake of library
,'liberry' # mistake of library
,'lisence' # mistake of license
,'lightening' # mistake of lightning
,'loose' # mistake of lose
,'maintainance' # mistake of maintenance
,'maintnance' # mistake of maintenance
,'marshmellow' # mistake of marshmallow
,'medeval' # mistake of medieval
,'medevil' # mistake of medieval
,'mideval' # mistake of medieval
,'momento' # mistake of memento
,'millenium' # mistake of millennium
,'milennium' # mistake of millennium
,'miniture' # mistake of miniature
,'miniscule' # mistake of minuscule
,'mischievious' # mistake of mischievous
,'mischevous' # mistake of mischievous
,'mischevious' # mistake of mischievous
,'mispell' # mistake of misspell
,'misspel' # mistake of misspell
,'neccessary' # mistake of necessary
,'necessery' # mistake of necessary
,'necesary' # mistake of necessary
,'neice' # mistake of niece
,'nieghbor' # mistake of neighbour
,'noticable' # mistake of noticeable
,'occassion' # mistake of occasion
,'occasionaly' # mistake of occasionally
,'occassionally' # mistake of occasionally
,'occurrance' # mistake of occurrence
,'occurence' # mistake of occurrence
,'occured' # mistake of occurred
,'ommision' # mistake of omission
,'omision' # mistake of omission
,'optimisation' # mistake of optimization
,'optimise' # mistake of optimize
,'orignal' # mistake of original
,'outragous' # mistake of outrageous
,'overriden' # mistake of overridden
,'parliment' # mistake of parliament
,'passtime' # mistake of pastime
,'pasttime' # mistake of pastime
,'percieve' # mistake of perceive
,'perseverence' # mistake of perseverance
,'personell' # mistake of personnel
,'personel' # mistake of personnel
,'plagerize' # mistake of plagiarize
,'playright' # mistake of playwright
,'playwrite' # mistake of playwright
,'posession' # mistake of possession
,'possesion' # mistake of possession
,'potatos' # mistake of potatoes
,'preceed' # mistake of precede
,'presance' # mistake of presence
,'principal' # mistake of principle
,'privelege' # mistake of privilege
,'priviledge' # mistake of privilege
,'professer' # mistake of professor
,'protestor' # mistake of protester
,'promiss' # mistake of promise
,'pronounciation' # mistake of pronunciation
,'prufe' # mistake of proof
,'publically' # mistake of publicly
,'quarentine' # mistake of quarantine
#,'que' # mistake of queue # more common as a non-English word
,'questionaire' # mistake of questionnaire
,'questionnair' # mistake of questionnaire
,'readible' # mistake of readable
,'realy' # mistake of really
,'recieve' # mistake of receive
,'reciept' # mistake of receipt
,'recomend' # mistake of recommend
,'reccommend' # mistake of recommend
,'refered' # mistake of referred
,'referance' # mistake of reference
,'refrence' # mistake of reference
,'relevent' # mistake of relevant
,'revelant' # mistake of relevant
,'religous' # mistake of religious
,'religius' # mistake of religious
,'repitition' # mistake of repetition
,'restarant' # mistake of restaurant
,'restaraunt' # mistake of restaurant
,'rime' # mistake of rhyme
,'rythm' # mistake of rhythm
,'rythem' # mistake of rhythm
,'secratary' # mistake of secretary
,'secretery' # mistake of secretary
,'sieze' # mistake of seize
,'seperate' # mistake of separate
,'sargent' # mistake of sergeant
,'similer' # mistake of similar
,'skilfull' # mistake of skilful
,'speach' # mistake of speech
,'succesful' # mistake of successful
,'successfull' # mistake of successful
,'sucessful' # mistake of successful
,'supercede' # mistake of supersede
,'suprise' # mistake of surprise
,'surprize' # mistake of surprise
,'tomatos' # mistake of tomatoes
,'tommorow' # mistake of tomorrow
,'tommorrow' # mistake of tomorrow
,'twelth' # mistake of twelfth
,'tyrany' # mistake of tyranny
,'udpate' # mistake of update
,'underate' # mistake of underrate
,'unecessary' # mistake of unnecessary
,'unneccessary' # mistake of unnecessary
,'unnecesary' # mistake of unnecessary
,'untill' # mistake of until
,'upholstry' # mistake of upholstery
,'usible' # mistake of usable/useable
,'vaccuum' # mistake of vacuum
,'vaccum' # mistake of vacuum
,'vacume' # mistake of vacuum
,'vehical' # mistake of vehicle
,'visious' # mistake of vicious
,'wether' # mistake of weather
#,'whether' # mistake of weather # removed - valid word
#,'wich' # mistake of which - Also a name
,'wierd' # mistake of weird
,'wellfare' # mistake of welfare
,'welfair' # mistake of welfare
,'wether' # mistake of whether
,'wilfull' # mistake of wilful
,'withold' # mistake of withhold
,'writting' # mistake of writing
,'writeing' # mistake of writing
]


excluded_terms = ['__PLACE_HOLDER__']


def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_typo(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def typo_to_bq():
    concept = 'typo'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_{concept}(message)".format(schema=SCHEMA_NAME
                                                       , concept=concept))
    # Spelling mistakes are local, no need to exclude by context
    print("# end - " + concept)

    #print(" - ")
    #print("# " + concept +  ": Excluded")
    #print("{schema}.bq_excluded_{concept}(message)".format(schema=SCHEMA_NAME
    #                                                       , concept=concept))

    #print(" - ")
    #print("# " + concept +  ": not positive")
    #print("{schema}.bq_not_positive_{concept}(message)".format(schema=SCHEMA_NAME
    #                                                               , concept=concept))

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concept = 'typo'

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
                         , typo_to_bq
                         , commit=commit)
    print()
def evaluate_typo_classifier():

    evaluate_concept_classifier(concept='Typo'
                                , text_name='message'
                                , classification_function=is_typo
                                , samples_file=join(DATA_PATH, 'commit_typos_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='00e2683072911effb4d82daff17f961bb2e9c94e')
    evaluate_typo_classifier()

    text = """
"WIP: Refactor KConfigXT

Summary:
The current KConfigXT compiler is in a sad state:
It's a massive file with loads of global variables that handle state, the generator is done within the main() function and it seems to have grown organically. There are no classes to separate logic / state / generation, what exists is code that generates code from a xml / ini pair, but it's hard to even discover what a bit of code is doing. The code istyle is C++ / Java from the nineties, which is not bad per see but it also uses quite a few things that are going to be deprecated in Qt 6 so I'm also taking the time make the code more streamlined with newer code style (no iterators, lambdas, auto usage, etc).

The code that generates the files simplly pushes strings to a text stream, and it's hard to figure out when something starts or something ends: for instance, the code that generates the Constructor has more than sixty lines of code englobing some nested if - for - if - for constructs.

Currently the code is ""done"" - there's one bug that I still need to find & fix regarding Translations, but the rest seems sane.
The current testcode generates incorrect *whitespaces* regarding the old code (there's some parts that I feel that it's important to fix before merging, but overall, the whitespace changes are not bad and easier to handle, old code had a hand-counted amount of spaces before each line, new code has a function whitespace() that adds the current-and-correct amount of whitespaces based on indentation level that you start by startScope() and ends with endScope(). rest of the code still needs to be ported to it.

I plan to fix the testcases whitespace by manually adding them, I'v fougth with the code for a while and added a few hacks there but I don't want to make the code hackish again.

New code is not perfect by any means, but is a good step in the right direction.

This code tries to Separate the compiler code into many different files / classes to be more obvious what's happening, and each class also has many helper methods to minimize copypaste.

  -     CodeGenerator: Has base code for the header and source files that can be shared
  -     HeaderGenerator: Logic for generating the header file
  -     SourceGenerator: Logic for generating the source file
  -     KcfgParser: Logic for parsing the kcfg file and extracting the information from the Xml file
  -     CommonStructs: a header that contains the structs that are currently used everywhere.
  -     KConfigParameters: (was CfgConfig - ConfigConfig, wat) - Has information passed via the kcfgc file
  -     kcfg_compiler - will be renamed to main - start the other classes and generates the files.

This code here currently has the begining of this separation, with the CodeGenerator and the HeaderGenerator in a ~good~ state, but unfinished.

Test Plan:
- Run the test cases,
- Compare the diffs generated by the testcases and fix in the code the errors / differences
- Run and compare real kde source with the new and old generators to look for errors

Reviewers: #frameworks, ervin, bport, dfaure

Reviewed By: dfaure

Subscribers: bport, ngraham, kde-frameworks-devel

Tags: #frameworks

Differential Revision: https://phabricator.kde.org/D26202
"

""".lower()
    print("is typo", is_typo(text))
    print("typo in text", re.findall(build_positive_regex(), text))


print(build_sepereted_term(positive_terms))