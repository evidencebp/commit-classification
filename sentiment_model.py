# Based on dictionary of SentiStrenght-SE from https://laser.cs.uno.edu/Projects/Projects.html
#


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH\
 , programming_languges
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

positive_sentiment = ['advantage',
 'adventurous',
 'amazing',
 'appease',
 'appreciat(?:e|es|ed|ing)',
 'attract(?:s|ed|ing|ive)?',
 'award(?:s|ed|ing)?',
 'awesome',
 'beaut(y|iful)',
 'beloved',
 'benefit(?:s|ed|ing)?',
 'beneficial',
 #'best',
 #'better', # usually more description than sentiment
 'bless(?:s|ed|ing)?',
 'blissful',
 'bonus',
 #'boost', # usually decriptive in software
 'calm(?:s|ed|ing)?',
 'charm(?:s|ed|ing)?',
 'cheer(?:s|ed|ing)?',
 'cheerful',
 'clever',
 'comfort(?:s|ed|ing|able)?',
 'confidence',
 'confident',
 'congratula(?:te|tion|tions)',
 'cool',
 'courtesy',
 'creative',
 'cute',
 'darling',
 'dear',
 'delectable',
 'deligh(?:t|ted)',
 'desirable',
 'desperat(?:e|es|ed|ing)',
 'devot(?:e|es|ed|ing)',
 #'ease', # consider
 #'easy', # consider
 'elegan(?:t|ce)',
 'encourag(?:e|es|ed|ing|ment)',
 'energetic',
 'enjoy(?:s|ed|ing)?',
 'entertaining',
 'enthus(?:iast|tic|tically)',
 'excellence',
 'excellent',
 'excit(?:ed|ing|es|ment)',
 'exuberant(?:s|ed|ing|ly)?',
 'fabulous(?:es|ly)?',
 'fame',
 'fantastic(?:ly)?',
 'fascinating',
 'favored',
 'favorite',
 'fine',
 'fond',
 'forgiv(?:e|es|ed|ing|ment)',
 #'freedom', # degrees of freedom
 'friendly',
 'fun',
 'funky',
 'funny',
 'futile',
 'genero(?:us|usly)',
 'glad',
 'glorified',
 'glory',
 'good',
 'goodness',
 'gorgeous',
 'grace',
 'gracious',
 'grand',
 'great',
 'greater',
 'greatest',
 'greet',
 'greeting',
 'happi(?:ness|ly)',
 'happy',
 'healthy',
 'heartwarming',
 'hero(?:s)?',
 'honor', # consider
 'honorabl(?:y|e)',
 #'hope',
 #'hopeful',
 #'hopefully',
 'hug',
 #'huge', # consider
 'hurtl(?:e|es|ed|ing)',
 'immune',
 #'importance', # consider
 #'important', # consider
 'impress(?:es|ed|ing|ive)?',
 'impression(?:s)?',
 'indestructible',
 #'inspir(?:es|ed|ing|ingly)?', # consider
 'intelligent',
 'intense',
 #'interest(?:ed|ing|ingly)?',
 #'invite', # consider
 'invulnerable',
 'jok(?:e|es|ing)',
 'joll(?:y|iness)',
 'joy(?:full)?',
 'justice',
 'justified',
 'keen',
 #'kind', # Commonly used as type
 'kindly',
 'kiss(?:es|ed|ing)?',
 'kudos',
 'laugh(?:es|ed|ing)?',
 #'legal',
 #'legally',
 #'lenient',
 #'like', # TODO - too common as similarity, not sentiment
 'lively',
 'lol',
 'love',
 'lovely',
 'luck',
 'lucked',
 #'lucki*',
 'lucks',
 'lucky',
 #'meaningful', # consider - might be descriptive
 'merry',
 #'motivation', # messages with structure "motivation: xxx"
 'natural', #consider
 'nice(?:r|st)?',
 'nifty',
 'noble',
 'optimistic', # consider optimistic scheduling
 'pardon',
 'peace',
 'perfect(?:s|ed|ing|ly)?',
 'perfectionis(?:it|m)',
 'piss(?: |-)?up',
 'pleasant(?:ful|ly)?',
 'pleased',
 'pleasure',
 'popularity',
 'positive',
 'positively',
 'powerful',
 'prett(?:ier|iest|y)',
 'privileged',
 #'promis(?:e|ing)', # consider
 'prospect',
 'proudly',
 'rejoice',
 'relieve',
 'rescue',
 #'respected', # consider
 #'restful', # Ahmmm, REST api...
 'revive',
 'reward',
 #'rich', # consider
 'rigorously',
 'safely',
 'salient',
 'satisfying',
 'scoop',
 'slick',
 'slicker',
 'smart(?:er|s|ly)',
 'smile',
 'soothe',
 'sophisticated',
 #'spark', # consider removing Aphace spark
 'sparkle',
 'spirit',
 #'strength',
 #'strengthen',
 #'strong', # consider
 'substantially',
 #'success',
 #'successful', # consider
 'sunshine',
 'superior',
 'survivor',
 'sweet',
 'thank',
 'thanked',
 'thanks',
 'thanx',
 'tnx',
 'tolerant',
 #'top', # consider
 'triumph',
 #'trust', # consider
 #'unbiased', # problematic in machine learning context
 'usefulness',
 #'vision', # consider
 #'warm', #consider
 'welcome',
 #'win', # consider (win size refers to a window)
 #'winner',
 'wonderful',
 'woo',
 'worth', # consider
 'worthy',
 #'wow', # consider
 #'yes', # Too common, not a strong sentiment
 'zealous']

negative_sentiment = ['abject',
 'abus(?:e|es|ed|ing|ive)',
 'afraid',
 'aghast',
 #'alarm(?:s|ed|ing)?', # consider
 'alas',
 'anger(?:s|ed|ing)?',
 'angry',
 'anno(?:y|ying|yed|edly)',
 'anti',
 'apolog(?:ize|ies|y)',
 'ashamed',
 'ass(?: |-)?hole(?:s)?',
 'attack(?:s|ed|ing)?',
 'awful(?:ly)?',
 'awkward(?:ly)?',
 'bad', # consider, might be descriptive
 'badly',
 'bastard',
 # 'battle', # consider
 'betra(?:y|ies|ied|ing)',
 #'bg', # too short, different meanings
 'bitch',
 'bizarre',
 'blam' + VERB_E_SUFFIX,
 'bloody',
 'blury',
 'bor(?:e|es|ed|ing)',
 #'boring*', Covered by above
 'bother(?:s|ed|ing)?',
 'bullshit',
 'burden',
 #'cancel*', - too common, low sentiment if anny
 'careless(?:ly)?',
 'casualty',
 'catastroph(?:e|y)',
 #'challenge', # consider
 'chaos',
 'chaotic(?:ly)?',
 'cheat' + REGULAR_SUFFIX,
 'choke' + VERB_E_SUFFIX,
 'complain' + REGULAR_SUFFIX,
 'confus' + VERB_E_SUFFIX,
 'contentious',
 'controvers(?:y|ial)',
 'crap',
 'crazy',
 #'critici*', # Meaning not clear
 'cruel(?:ty)?',
 'crush',
 'cry',
 'curs' + VERB_E_SUFFIX,
 'cynical(?:ly)',
 #'damag' + VERB_E_SUFFIX, # used as descriptive to content
 'damn',
 'danger(?:ously|ous)?',
 'deadly',
 #'death',
 'degrad' + VERB_E_SUFFIX,
 'demean' + REGULAR_SUFFIX,
 'depress(?:ed|ing|ion)?',
 'despise',
 #'destro(?:y|ing|ied)', # common due to object destruction, destructors
 #'destruction', # common due to object destruction, destructors
 #'dickhead',  # We have a dedicated swearing model
 'difficult(?:y|ies)?',
 'dilemma',
 'dirt',
 #'dirty', # refers to dirty software objects
 'disadvantage(?:s)?',
 'disappoint' + VERB_E_SUFFIX,
 'disaster',
 'disastrous',
 'disgust' + REGULAR_SUFFIX,
 'dislik' + VERB_E_SUFFIX,
 'dismal',
 'dispute',
 'disregard' + REGULAR_SUFFIX,
 'disrupt(?:s|ed|ing|ion)?',
 'distort(?:s|ed|ing|ion)?', # consider
 'distract(?:s|ed|ing|ion)?',
 'distress' + REGULAR_SUFFIX,
 'disturb' + REGULAR_SUFFIX,
 'dodgy',
 'doh',
 'doom' + REGULAR_SUFFIX,
 'doubt(?:s|ed|ing|full)?',
 'downcast',
 'downhearted',
 'dread(?:s|ed|ing|full)?',
 #'drop', # drop table
 'dubious(?:ly)',
 'dumb',
 'dupe',
 #'eager', # also software term eager/lazy evaluation
 'earnest',
 'embarrass(?:ment|ed|ing|es)?',
 'emergency',
 'emptiness',
 'evil',
 'fear',
 '(fight|fought|fights|fighting)',
 'flop',
 'fool' + REGULAR_SUFFIX,
 'foolish',
 #'forgotten', # consider
 'frantic',
 'freak'  + REGULAR_SUFFIX,
 'frenzy',
 'fright(?:en|ned|ning|s)?',
 'frustrat' + VERB_E_SUFFIX,
 'frustrating',
 'frustration',
 #'fuck', # We have a dedicated swearing model for that
 'furious(?:ing|es|ed|ly)?',
 #'ghost', # consider
 #'goddam',# We have a dedicated swearing model for that
 #'grave(?:s)?', # Also a last name
 #'greed', # also a software trem, greedy algorithm
 #'greedy', # also a software trem, greedy algorithm
 #'grey', # Common simply as the color
 'grief',
 #'gross', #different meanings
 'guilt(?:y)?',
 #'hard', # also a software trem, hard rest
 'harm',
 'harmed',
 'harmful(?:ly)?',
 'harming',
 'harsh',
 'hate',
 'hated',
 'hateful(?:ly)?',
 'hater(?:s)?',
 'hates',
 'hating',
 'hatred',
 'havoc',
 'hell',
 'hopeless',
 'horrendous',
 'horrifing',
 'horrible',
 'horror',
 'hostile',
 'hurt(?:s|ing)?',
 'hysteria',
 'idioc(?:y)?',
 'idiot(?:ic)?',
 'ignoble',
 #'ignor*', # catches ignore
 'ignorance',
 #'ignore*', # catches ignore
 'ill',
 'inability',
 'inadequa(?:cy|te|ly)',
 'inconvenience',
 'inconvenient',
 'ineffective',
 'inferior(?:ly)?',
 'insane',
 'insanity',
 #'insecur*', # more common as non sentiment in software
 #'insensitive', # case insensitive
 #'insignificant', # consider
 'intimidat' + VERB_E_SUFFIX,
 'irreversible', # consider
 'irrita(?:able|tion)',
 'jumpy',
 'lame',
 'lament(?:ation)?',
 'laughable',
 'laughingstock',
 'loathing',
 #'lobby', # consider
 'lonely',
 'loser',
 #'loss', # common in software, e.g., loss function
 #'lost', # consider
 'lurk',
 'mad',
 'madness',
 'meaningless',
 'mess(?:y|es|ed|ing)?',
 'mindless',
 'misbehav' + VERB_E_SUFFIX,
 'misbehavior',
 'mischief',
 'miser(?:y|able)',
 #'misinformation', # might be no sentimanet in software
 'misleading',
 'misread',
 #'mistak(?:e|ed|es|en)', # might be no sentimanet in software
 'misunder(?:stand|stood)',
 'misunderstanding',
 'moan(?:s|ed|ing)?',
 #'moron', # We have a dedicated swearing model for that
 'murder(?:er|ous)?',
 'nast(?:y|iest)?',
 #'naive*', # check original value - unicode?
 'negligen(?:ce|cly)',
 'nervous(?:ly)?',
 'non(?:-|\s)?sens(?:e|ly)',
 'obliterat' + VERB_E_SUFFIX,
 'obnoxious(?:ly)?',
 'obscene',
 'odd',
 'offend' + REGULAR_SUFFIX,
 #'offended', # covered in the term above
 'offender',
 #'oop', Object Oriented Programming
 'oops',
 'oppress' + REGULAR_SUFFIX,
 'outrag(?:e|es|ed|ing|eous)',
 'oversimplify',
 'pain',
 'panic(?:ally)?',
 'pathetic(?:ally)?',
 'peril(?:ous)?',
 'pesky',
 'pessimis(?:tic|tically)',
 'piss',
 'piti',
 'pity',
 'poison(?:s|ed|ing|ly|ous)?',
 'polluted',
 'poor',
 'possessive',
 'pretend',
 'provoke',
 'rage',
 'rainy',
 'rant',
 'rash',
 'refused',
 'regret(?:fully|ing|s|ed)?',
 'resign',
 'retreat',
 'ridiculous(?:ly)?',
 'rig',
 #'rip', # consider
 'ruin',
 'sad',
 'sadly',
 'scare',
 'scary',
 'scream' + REGULAR_SUFFIX,
 'screw(?:s|ed|ing)?',
 'severe(?:ly)?',
 'severity',
 'shaky',
 'sham(?:eful|efully|eless|elessly|es|ed|ing)?',
 #'shit*', # We have a dedicated swearing model for that
 #'shitty', # We have a dedicated swearing model for that
 'shock' + REGULAR_SUFFIX,
 '(shoot|shot|shoots|shooting)',
 'shy',
 'sick',
 'silly',
 'skeptic(?:ly)?',
 'sluggish(?:ly)?',
 'smear(?:y|s|ed|ing)?',
 'sneaky',
 'sore',
 'sorry',
 'speculative',
 #'stab' + REGULAR_SUFFIX, # consider
 #'stalled', # common as descriptive
 'stalling',
 #'starve' + VERB_E_SUFFIX,
 #'starvation', # starvation happens in programming
 #'starving',
 '(steal|stole|steals|stealing)',
 'stealth',
 'strange',
 'strangely',
 'stressed',
 'struggle',
 'stuck',
 'stupid',
 'stupidly',
 'suck' + REGULAR_SUFFIX,
 #'sucks', # covered above
 'suffer',
 'suicidal',
 'suspect',
 'suspicious',
 '(swear|swaers|swore|swearing)',
 #'swearing',
 'terrible',
 'terribly',
 'threat',
 'threatening',
 'tired',
 'torture',
 'trap',
 'trauma(?:tic)?',
 'trickery',
 'trouble',
 'ugly',
 'uhh',
 'unacceptable',
 'unbelievable',
 'uncertain',
 #'unclear',
 'uncomfortable',
 'undecided',
 'underestimate',
 'undesirable',
 'uneasy',
 'unfocused',
 'unfortunate(?:ly)?',
 'unhappy',
 'unhealthy',
 'unloved',
 'unsatisfied',
 'unwanted',
 'upset',
 'useless',
 'vicious',
 'vile',
 'violent',
 'wast' + VERB_E_SUFFIX,
 #'wasting',
 #'weak', # consider
 'weakness',
 'weird',
 'wicked',
 'woops',
 'worry',
 'worrying',
 'worse',
 'worsen',
 'worst',
 'worthless',
 'wreck',
 'wtf']

excluded_positive_sentiment=['trust me', 'best effort', 'on top', 'pretty(?:-|\s)print(?:er|ers|ing|ed|s)?'
 , 'pretty(?:-|\s)format(?:er|ing|ed|s)?', 'top level(?:s)?', '(make|makes|made|making)' + NEAR_ENOUGH + 'happy'
 , 'rich text', 'warm reset', '(false|true) positive(:?s)?', 'worth (doing|keeping|it)'
 , 'respected for (' + "|".join(programming_languges) + ")"
 , 'degrees of freedom', "I'm pretty", "I am pretty", 'positive (integer|number)', 'perfectly (good|ok|valid)'
 , 'work(:?s|ed|ing)? fine', '(take|took|taking) advantage', 'making good sense', 'user friendly', 'smart annotation'
 , 'at best', "(we|we're|I|I'm|you|you're|he|he's|she's) good", 'greater than', 'greater'+ NEAR_ENOUGH +'equal'
 , "third time's the charm", 'good faith', 'good riddance', 'for good', 'good to have', 'probably good', 'good enough'
 , 'usually good', 'good match', 'good data'
 , 'pretty (sure|common|commonly|long|much|likely|unlikely|simple|straight(?:-|\s)?forward|big|small|useless)'
 , 'pretty (active|dead|misleading|expensive|trivial|ugly|hard|often|embarrassing|similar|complex)'
 , "'pretty'", '"pretty"'
 , 'best to', 'best(?:-|\s)practice(:?s)?', 'best(?:-|\s)effort(:?s)?', 'the best of', 'best regards'
 , 'fine grain(:?ed)?', 'fine tun(:?e|ed|esing)', '(the|a) best case'
 , 'good state' # consider
 , 'for good' # consider
 #, 'good idea(s)?' # consider
                             ]
excluded_negative_sentiment=['paranoia code', "april fool's", "april fool", '(false|true) negative(:?s)?', 'snmp trap'
 , 'kernel panic', 'fix panic' # more like "fix kernel panic
 , 'bad service error', 'bad data', 'dirty (state|range|bit(?:s)?)', '(the|a) worse case'

 #, 'quick and dirty' #This is actually a sentiment
                             ]


def build_positive_sentiment_regex():

    return build_sepereted_term(positive_sentiment)



def build_positive_sentiment_excluded_regex():

    return build_sepereted_term(excluded_positive_sentiment)

def build_not_positive_sentiment_regex():

    return build_non_positive_linguistic(build_positive_sentiment_regex())


def is_positive_sentiment(commit_text):

    return (len(re.findall(build_positive_sentiment_regex(), commit_text))
            - len(re.findall(build_positive_sentiment_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_sentiment_regex(), commit_text)))  > 0



def positive_sentiment_to_bq():
    concept = 'positive_sentiment'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_positive_sentiment(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_positive_sentiment(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_sentiment(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)


# Negative sentiment

def build_negative_sentiment_regex():

    return build_sepereted_term(negative_sentiment)



def build_negative_sentiment_excluded_regex():

    return build_sepereted_term(excluded_negative_sentiment)

def build_not_negative_sentiment_regex():

    return build_non_positive_linguistic(build_negative_sentiment_regex())


def is_negative_sentiment(commit_text):

    return (len(re.findall(build_negative_sentiment_regex(), commit_text))
            - len(re.findall(build_negative_sentiment_excluded_regex(), commit_text))
            - len(re.findall(build_not_negative_sentiment_regex(), commit_text)))  > 0



def negative_sentiment_to_bq():
    concept = 'negative_sentiment'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_negative_sentiment(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_negative_sentiment(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not negative")
    print("{schema}.bq_not_negative_sentiment(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)



def print_concepts_functions_for_bq(commit: str = 'XXX'):


    concepts = {
        'core_positive_sentiment' : build_positive_sentiment_regex
        , 'excluded_positive_sentiment': build_positive_sentiment_excluded_regex
        , 'not_positive_sentiment' : build_not_positive_sentiment_regex
        #, 'good': positive_sentiment_to_bq
        , 'core_negative_sentiment': build_negative_sentiment_regex
        , 'excluded_negative_sentiment': build_negative_sentiment_excluded_regex
        , 'not_negative_sentiment': build_not_negative_sentiment_regex
        # , 'good': positive_sentiment_to_bq

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
                                                        , concept='positive_sentiment')
                         , positive_sentiment_to_bq
                         , commit=commit)
    print()

    generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                        , concept='negative_sentiment')
                         , negative_sentiment_to_bq
                         , commit=commit)
    print()

if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='8ffb7b7b5b90fa5917fe08b8310bc3d5a28b898c')


    text = """
"Improve Phan's ability to track unconditionally true/false branches.

And be stricter about how static blocks are analyzed.
Stop treating static variables without defaults as having the empty
union type.

Phan works best when the definitions of static variables are above their
uses.

```
static $a;
static $b;
if ($a === null) {
    $a = e();
    $b = expr();
}
use ($a, $b);
```
"
  """.lower()
    print(is_positive_sentiment(text))
    valid_num = len(re.findall(build_positive_sentiment_regex(), text))
    print(re.findall(build_positive_sentiment_regex(), text))
    print("neg", re.findall(build_not_positive_sentiment_regex(), text))
    print("ex", re.findall(build_positive_sentiment_excluded_regex(), text))


    print("s1", re.findall('pretty(?:-|\s)print(?:er|ing|ed|s)?', text))


"""
 Better safe than sorry
 Update editor mobile message with sad smile

"""