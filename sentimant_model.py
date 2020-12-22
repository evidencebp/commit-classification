# Based on dictionary of SentiStrenght-SE from https://laser.cs.uno.edu/Projects/Projects.html
#


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

positive_sentiment = ['advantage',
 'adventurous',
 'amaz*',
 'appease',
 'appreciat*',
 'attract*',
 'award*',
 'awesome*',
 'beaut*',
 'beloved*',
 'benefit*',
 'best',
 'better',
 'bless*',
 'blissful',
 'boost',
 'calm*',
 'charm*',
 'cheer*',
 'cheerful*',
 'clever',
 'comfort*',
 'confidence',
 'confident',
 'congratula*',
 'cool',
 'courtesy',
 'creative',
 'cute*',
 'darlin*',
 'dear',
 'delectabl*',
 'deligh*',
 'desirable',
 'desperat*',
 'devot*',
 'ease*',
 'easy',
 'elegan*',
 'encourag*',
 'energetic',
 'enjoy*',
 'entertaining',
 'enthus*',
 'excellence',
 'excellent',
 'excit*',
 'exuberan*',
 'fabulous*',
 'fame',
 'fantastic*',
 'fascinating',
 'favored',
 'favorite',
 'fine',
 'fond',
 'forgiv*',
 'forgiving',
 'freedom',
 'friendly',
 'fun',
 'funky',
 'funny',
 'futile',
 'genero*',
 'glad',
 'glori*',
 'glory',
 'good',
 'goodness',
 'gorgeous',
 'grace',
 'graci*',
 'grand',
 'great*',
 'greater',
 'greatest',
 'greet',
 'greeting',
 'happi*',
 'happy',
 'healthy',
 'heartwarm*',
 'hero*',
 'honor',
 'honorabl*',
 'hope',
 'hopeful',
 'hopefully',
 'hug',
 'huge',
 'hurtl*',
 'immune',
 'importance',
 'important',
 'impress*',
 'impression*',
 'indestructible',
 'inspir*',
 'intelligent*',
 'intense',
 'interest*',
 'invite',
 'invulnerable',
 'joke*',
 'joll*',
 'joy*',
 'justice',
 'justified',
 'keen',
 'kind',
 'kindly',
 'kiss*',
 'kudos',
 'laugh*',
 'legal',
 'legally',
 'lenient',
 'like',
 'lively',
 'lol',
 'love',
 'lovely',
 'luck',
 'lucked',
 'lucki*',
 'lucks',
 'lucky',
 'meaningful',
 'merry',
 'motivation',
 'natural',
 'nice*',
 'nifty',
 'noble',
 'optimistic*',
 'pardon',
 'peace*',
 'perfect*',
 'perfectionis*',
 'pissup*',
 'pleasant*',
 'pleased',
 'pleasure',
 'popularity',
 'positive',
 'positively',
 'powerful',
 'prettie*',
 'privileged',
 'promis*',
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
 'smart*',
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
 'abusi*',
 'afraid',
 'aghast',
 'alarm*',
 'alas',
 'anger*',
 'angr*',
 'annoy*',
 'anti*',
 'apolog*',
 'ashamed',
 'asshole*',
 'attack*',
 'awful*',
 'awkward*',
 'bad',
 'badly',
 'bastard*',
 'battle*',
 'betray*',
 'bg',
 'bitch*',
 'bizarre',
 'blam*',
 'bloody',
 'blur*',
 'bore*',
 'boring*',
 'bother*',
 'bullshit',
 'burden*',
 #'cancel*', - too common, low sentiment if anny
 'careless*',
 'casualty',
 'catastroph*',
 'challenge',
 'chaos',
 'chaotic*',
 'cheat*',
 'choke*',
 'complain*',
 'confus*',
 'contentious',
 'controvers*',
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



def build_positive_sentiment_regex():

    return build_sepereted_term(positive_sentiment)



def build_positive_sentiment_excluded_regex():

    return build_sepereted_term(positive_sentiment)

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

    return build_sepereted_term(negative_sentiment)

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
    #print_concepts_functions_for_bq(commit=None)

    text = """when a Route is removed, don't bother triggering a sync-presentation-info-from-treeview because it isn't necessary

Also, don't update mixer selection unless selection actually changed""".lower()

    print(is_positive_sentiment(text))
    valid_num = len(re.findall(build_positive_sentiment_regex(), text))

