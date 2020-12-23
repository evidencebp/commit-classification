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
 'better',
 'bless(?:s|ed|ing)?',
 'blissful',
 'boost',
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
 'easy',
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
 'legal',
 'legally',
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
 'bad',
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
 'critici*',
 'cruel*',
 'crush',
 'cry',
 'curse*',
 'cyni*',
 'damag*',
 'damn*',
 'danger*',
 'deadly',
 'death*',
 'degrad*',
 'demean*',
 'depress*',
 'despise',
 'destroy*',
 'destruct*',
 'dickhead*',
 'difficult*',
 'dilemma',
 'dirt',
 'dirty',
 'disadvantage*',
 'disappoint*',
 'disaster*',
 'disastrous*',
 'disgust*',
 'dislike*',
 'dismal',
 'dispute',
 'disregard*',
 'disrupt*',
 'distort*',
 'distract*',
 'distress*',
 'disturb*',
 'dodgy',
 'doh',
 'doom*',
 'doubt*',
 'downcast',
 'downhearted*',
 'dread*',
 'drop',
 'dubious*',
 'dumb*',
 'dupe',
 'eager*',
 'earnest',
 'embarrass*',
 'emergency',
 'emptiness',
 'evil*',
 'fear',
 'fight*',
 'flop',
 'fool*',
 'foolish',
 'forgotten',
 'frantic*',
 'freak*',
 'frenzy',
 'fright*',
 'frustrat*',
 'frustrating',
 'frustration',
 'fuck',
 'fuck*',
 'fucked*',
 'fucker*',
 'fuckface',
 'fucking',
 'fucks',
 'furious*',
 'ghost',
 'goddam*',
 'grave*',
 'greed*',
 'greedy',
 'grey',
 'grief',
 'gross*',
 'guilt*',
 'hard',
 'harm',
 'harmed',
 'harmful*',
 'harming',
 'harsh',
 'hate',
 'hated',
 'hateful*',
 'hater*',
 'hates',
 'hating',
 'hatred',
 'havoc',
 'hell',
 'hopeless',
 'horrendous',
 'horri*',
 'horrible',
 'hostile',
 'hurt*',
 'hysteria',
 'idioc*',
 'idiot',
 'idiot*',
 'ignoble',
 'ignor*',
 'ignorance',
 'ignore*',
 'ill',
 'inability',
 'inadequa*',
 'inconvenience',
 'inconvenient',
 'ineffective',
 'inferior*',
 'insane',
 'insanity',
 'insecur*',
 'insensitive',
 'insignificant',
 'intimidat*',
 'irreversible',
 'irrita*',
 'jumpy',
 'lame*',
 'lament*',
 'laughable',
 'laughingstock*',
 'loathing',
 'lobby',
 'lonely',
 'loser',
 'loss',
 'lost',
 'lurk',
 'mad',
 'madness',
 'meaningless',
 'mess*',
 'mindless',
 'misbehav*',
 'misbehavior',
 'mischief',
 'miser*',
 'misinformation',
 'misleading',
 'misread',
 'mistak*',
 'misunderstand',
 'misunderstanding',
 'moan',
 'moron*',
 'murder*',
 'nast*',
 #'naive*', # check original value - unicode?
 'negligen*',
 'nervous*',
 'nonsens*',
 'obliterate*',
 'obnoxious*',
 'obscene',
 'odd',
 'offend*',
 'offended',
 'offender',
 'oop',
 'oops',
 'oppress*',
 'outrage*',
 'oversimplify',
 'pain',
 'panic*',
 'pathetic*',
 'peril*',
 'pesky',
 'pessimis*',
 'piss*',
 'piti*',
 'pity*',
 'poison*',
 'polluted',
 'poor*',
 'possessive',
 'pretend',
 'provoke',
 'rage',
 'rainy',
 'rant',
 'rash',
 'refused',
 'regret*',
 'resign',
 'retreat',
 'ridicul*',
 'rig',
 'rip',
 'ruin',
 'sad',
 'sadly',
 'scare',
 'scary',
 'scream*',
 'screwed',
 'severe*',
 'severity',
 'shaky',
 'shame*',
 'shit*',
 'shitty',
 'shock*',
 'shoot*',
 'shy*',
 'sick',
 'silly',
 'skeptic*',
 'sluggish*',
 'smear*',
 'sneaky',
 'sore',
 'sorry',
 'speculative',
 'stab*',
 'stalled',
 'stalling',
 'starve*',
 'starving',
 'steal*',
 'stealth*',
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
 'trauma*',
 'trickery',
 'trouble',
 'ugly',
 'uhh',
 'unacceptable',
 'unbelievable',
 'uncertain',
 'unclear',
 'uncomfortable',
 'undecided',
 'underestimate',
 'undesirable',
 'uneasy',
 'unfocused',
 'unfortunate*',
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
 'weak',
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

PLACHOLDER = 'NON_EXISTIG_TEXT'
excluded_positive_sentiment=[PLACHOLDER]
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

    text = """Cut extraneous ^M.""".lower()

    print(is_positive_sentiment(text))
    valid_num = len(re.findall(build_positive_sentiment_regex(), text))
    print(re.findall(build_positive_sentiment_regex(), text))
    print(is_negative_sentiment(text))
    valid_num = len(re.findall(build_negative_sentiment_regex(), text))
    print(re.findall(build_negative_sentiment_regex(), text))

"""
 nautilus-clean.sh 
"""