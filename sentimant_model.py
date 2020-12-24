# Based on dictionary of SentiStrenght-SE from https://laser.cs.uno.edu/Projects/Projects.html
#


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX
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
 'best',
 #'better', # usually more description than sentiment
 'bless(?:s|ed|ing)?',
 'blissful',
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
 'ease',
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
 'freedom',
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
 'honor',
 'honorabl(?:y|e)',
 'hope',
 'hopeful',
 'hopefully',
 'hug',
 'huge',
 'hurtl(?:e|es|ed|ing)',
 'immune',
 'importance',
 'important',
 'impress(?:es|ed|ing|ive)?',
 'impression(?:s)?',
 'indestructible',
 'inspir(?:es|ed|ing|ingly)?',
 'intelligent',
 'intense',
 'interest(?:ed|ing|ingly)?',
 'invite',
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
 'lenient',
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
 'meaningful',
 'merry',
 'motivation',
 'natural',
 'nice(?:r|st)?',
 'nifty',
 'noble',
 'optimistic',
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
 'promis(?:e|ing)',
 'prospect',
 'proudly',
 'rejoice',
 'relieve',
 'rescue',
 'respected',
 'restful',
 'revive',
 'reward',
 'rich',
 'rigorously',
 'safely',
 'salient',
 'satisfying',
 'scoop',
 'slick',
 'slicker',
 'smart(?:er|s|ly)?',
 'smile',
 'soothe',
 'sophisticated',
 'spark',
 'sparkle',
 'spirit',
 'strength',
 'strengthen',
 'strong',
 'substantially',
 'success',
 'successful',
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
 'top',
 'triumph',
 'trust',
 'unbiased',
 'usefulness',
 'vision',
 'warm',
 'welcome',
 'win',
 'winner',
 'wonderful',
 'woo',
 'worth',
 'worthy',
 'wow',
 #'yes', # Too common, not a strong sentiment
 'zealous']

negative_sentiment = ['abject',
 'abus(?:e|es|ed|ing|ive)',
 'afraid',
 'aghast',
 'alarm(?:s|ed|ing)?',
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
 #'bad', # consider, might be descriptive
 'badly',
 'bastard',
 'battle',
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
 'challenge',
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
 'damag' + VERB_E_SUFFIX,
 'damn',
 'danger(?:ously|ous)?',
 'deadly',
 'death',
 'degrad' + VERB_E_SUFFIX,
 'demean' + REGULAR_SUFFIX,
 'depress(?:ed|ing|ion)?',
 'despise',
 'destro(?:y|ing|ied)',
 'destruction',
 'dickhead',
 'difficult(?:y|ies)?',
 'dilemma',
 'dirt',
 'dirty',
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
 'distort(?:s|ed|ing|ion)?',
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
 'forgotten',
 'frantic',
 'freak'  + REGULAR_SUFFIX,
 'frenzy',
 'fright(?:en|ned|ning|s)?',
 'frustrat' + VERB_E_SUFFIX,
 'frustrating',
 'frustration',
 #'fuck', # We have a dedicated swearing model for that
 'furious(?:ing|es|ed|ly)?',
 'ghost',
 #'goddam',# We have a dedicated swearing model for that
 'grave(?:s)?',
 #'greed', # also a software trem, greedy algorithm
 #'greedy', # also a software trem, greedy algorithm
 'grey',
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
 'insensitive',
 'insignificant',
 'intimidat' + VERB_E_SUFFIX,
 'irreversible',
 'irrita(?:able|tion)',
 'jumpy',
 'lame',
 'lament(?:ation)?',
 'laughable',
 'laughingstock',
 'loathing',
 'lobby',
 'lonely',
 'loser',
 #'loss', # common in software, e.g., loss function
 'lost',
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
 'misunderstand',
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
 'rip',
 'ruin',
 'sad',
 'sadly',
 'scare',
 'scary',
 'scream' + REGULAR_SUFFIX,
 'screwed',
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
 'stab' + REGULAR_SUFFIX,
 'stalled',
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
 'suck',
 'sucks',
 'suffer',
 'suicidal',
 'suspect',
 'suspicious',
 'swear',
 'swearing',
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
 'waste',
 'wasting',
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

excluded_positive_sentiment=['trust me']
excluded_negative_sentiment=['paranoia code']


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
    print_concepts_functions_for_bq(commit=None)

    text = """Redo my changes on Box

Hopefully this will fix the conflict with the fire alarms.
""".lower()

    print(is_positive_sentiment(text))
    valid_num = len(re.findall(build_positive_sentiment_regex(), text))
    print(re.findall(build_positive_sentiment_regex(), text))
    print(is_negative_sentiment(text))
    valid_num = len(re.findall(build_negative_sentiment_regex(), text))
    print(re.findall(build_negative_sentiment_regex(), text))

"""
 Better safe than sorry
 Update editor mobile message with sad smile

"""