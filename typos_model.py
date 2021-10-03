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
,'agrieve' # mistake of aggrieved
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
,'jason' # mistake of json (JSON format)
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
,'wich' # mistake of which
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
    print_concepts_functions_for_bq(commit='81e7b2f240ba39adde3d6ece4030d144fce19d50')
    evaluate_typo_classifier()

    text = """

"KVM: SVM: move nested svm state into seperate struct

This makes it more clear for which purpose these members in the vcpu_svm
exist.

Signed-off-by: Joerg Roedel <ebd221a096cbc71dd9e1991db28795933c85f380@amd.com>
Acked-by: Alexander Graf <3ad82b0c937b9aa51276120cedd545efc822be04@suse.de>
Signed-off-by: Avi Kivity <8f920f22884d6fea9df883843c4a8095a2e5ac6f@redhat.com>
"

""".lower()
    print("is typo", is_typo(text))
    print("typo in text", re.findall(build_positive_regex(), text))


print(build_sepereted_term(positive_terms))