# Design patterns list is based on wikipedia https://en.wikipedia.org/wiki/Software_design_pattern
import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH\
 , programming_languges, software_goals
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier


core_abstraction_terms = [
'abstraction',
'abtract'  + REGULAR_SUFFIX,
#'adapter(?:s)?', # specific components, consider
'adt',# Abstract Data Type
#'bridge(?:s)?',
'chain of responsibility',
'coherenc(?:e|y)',
'cohesion',
'composite',
'compos' + VERB_E_SUFFIX,
'composition',
'coupl(ed|ing)', # Note couples is missing since it common meaning is different
'controler(?:s)?',
'de(?: |-)?compos'  + VERB_E_SUFFIX,
'de(?: |-)?composition',
'de(?: |-)?coupl'  + VERB_E_SUFFIX,
'decorator(?:s)?',
'delegat' + VERB_E_SUFFIX,
'delegation',
'dependabilit(?:y|ies)',
'remov' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
#'dependenc(?:y|ies)',
'dependency injection',
'dependency inversion',
'design (?:decision|requirment|constraint)(?:s)?',
'design(?: |-)pattern(?:s)?',
'dry principle', # Don't Repeat Yourself
'(code|function|method) duplication',
'duplicat' + VERB_E_SUFFIX + NEAR_ENOUGH + '(code|function|method)',
'encapsulat' + VERB_E_SUFFIX,
'encapsulation',
'facade(?:s)?',
'factory',
'flyweight(?:s)?',
#'generic(?:s)?',
'(make|makes|making|made)' + NEAR_ENOUGH + '(private|public|protected|virtual)',
'more generic',
'generic type(?:s)?',
'inheritance',
'interface',
'interface segregation',
#'iterator(?:s)?', # too local and simple
'lazy initialization',
'liskov', # Liskov substitution principle
#'marker(?:s)?',
'mediator',
'memento',
'multiton',
'object(?:s)?(?: |-)pool(?:s)?',
'observer(?:s)?',
'object(?: |-)oriented',
'open(?: |-)closed principle',
'polymorphism',
#'prototype(?:s)?', # not relate to abstraction
#'prox(?:y|ies)', # mostly proxy servers
'publisher(?:s)?',
'pub(?: |-|/)sub',
're(?: |-)?us' + VERB_E_SUFFIX,
're(?: |-)?useability',
'refinement',
'reification',
'resource acquisition is initialization',
'raii', # Resource acquisition is initialization (RAII)
'single responsibility',
'singleton',
'solid', # SOLID principles
'structured programming',
'subscriber(?:s)?',
'servant',
#'specification(?:s)?', # consider
#'state(?:s)?', # consider
#'strateg(?:y|ies)', # consider
'sub(?:-| )?class(?:es)?',
'super(?:-| )?class(?:es)?',
#'template(?:s)?',
'testabil(?:e|ity)',
'twins(?:s)?',
#'translator(?:s)?', # more common for languages
'virtual method',
'visitor(?:s)?',
'(walker) state',
'wrapper(?:s)?',

]






excluded_abstraction_terms = ['reduc(es|e|ed|ing) abstraction'
, 'updat' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
, 'upgrad' + VERB_E_SUFFIX + NEAR_ENOUGH + 'dependenc(?:y|ies)'
, '(useless|bad) abstraction', 'user interface', 'interface binding', 'subscriber(?:s)?:', 'publisher(?:s)?:'
, "(we|you)'re using", 'wi(?: |-)?fi\sinterface','(flash|graphical|graphic) interface'
, 'use' + NEAR_ENOUGH + 'interface', 'event(?:s)? delegation'

                              ]

# Corrective
def build_core_abstraction_regex():

    return build_sepereted_term(core_abstraction_terms)



def build_excluded_abstraction_regex():

    return build_sepereted_term(excluded_abstraction_terms)


def build_not_abstraction_regex():

    return build_non_positive_linguistic(build_core_abstraction_regex())


def is_abstraction(commit_text):

    return (len(re.findall(build_core_abstraction_regex(), commit_text.lower()))
            - len(re.findall(build_excluded_abstraction_regex(), commit_text.lower()))
            - len(re.findall(build_not_abstraction_regex(), commit_text.lower()))
            )> 0



def print_abstraction_to_bq():
    concept = 'abstraction'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_abstraction(message)".format(schema=SCHEMA_NAME))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_abstraction(message)".format(schema=SCHEMA_NAME))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_abstraction(message)".format(schema=SCHEMA_NAME))
    print("# end - " + concept)


def print_abstractionfunctions_for_bq(commit: str = 'XXX'):

    concepts = {'core_abstraction' : build_core_abstraction_regex
                , 'excluded_abstraction': build_excluded_abstraction_regex
                , 'not_abstraction': build_not_abstraction_regex
                #, 'abstraction': print_abstraction_to_bq
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
                                                        , concept='abstraction')
                         , print_abstraction_to_bq
                         , commit=commit)


def evaluate_abstraction_classifier():
    text_name = 'message'
    classification_function = is_abstraction
    classification_column = 'abstraction_pred'

    concept_column = 'Is_abstraction'

    df = pd.read_csv(join(DATA_PATH, 'abstraction_commits.csv'))


    df = classifiy_commits_df(df
                              , classification_function=classification_function
                              , classification_column=classification_column
                              , text_name=text_name
                              )
    cm = evaluate_performance(df
                              , classification_column
                              , concept_column
                              , text_name=text_name)
    print("Abstraction labels CM")
    print(cm)

if __name__ == '__main__':
    print_abstractionfunctions_for_bq(commit='16a4cdc8bee84218f8767188f17c1394728092d5')
    #evaluate_cc_fix_classifier()

    text = """
"Migrate Cesium to ES6 Modules

See https://github.com/AnalyticalGraphicsInc/cesium/pull/8224 for details.

eslint
There are a handful of new .eslintrc.json files, mostly to identify the files that are still AMD modules (Sandcastle/Workers). These are needed because you can't change the parser type with a comment directive (since the parser is the thing reading the file). We can finally detect unusued modules! So those have all been cleaned up as well.

requirejs -> rollup & clean-css
requirejs, almond, and karma-requirejs have all been removed. We now use rollup for building and minifying (via uglify) JS code and clean-css for css. These changes are fairly straight-forward and just involve calling rollup instead of requirejs in the build process.

Overall build time is significantly faster. CI is ~11 minutes compared to ~17 in master. Running makeZipFile on my machine takes 69 seconds compared to 112 seconds in master. There's probably plenty of room for additional optimization here too.

We wrote an published a small npm module, rollup-plugin-strip-pragma, for stripping the requirejs pragmas we use out of the release builds. This is maintained in the Tools/rollup-plugin-strip-pragma directory.

As for what we produce. The built version of Cesium is now a UMD module. So it should work anywhere that hasn't made the jump to ES6 yet. For users that were already using the ""legacy"" combined/minified approach, nothing changes.

One awesome thing about roll-up is that it compiles all of the workers at once and automatically detects shared codes and generates separate bundles under the hood. This means the size of our worker modules shrink dramatically and Cesium itself will load them much faster. The total minified/gzipped size of all workers in master is 2.6 MB compared to 225 KB in this branch! This should be most noticeable on demos like Geometry & Appearances which load lots of workers for the various geometry typs.

roll-up is also used to build Cesium Viewer, which is now an ES6 app.

We use clean-css via gulp and it is also a straightforward change from requirejs that requires no special mention.

Workers
While the spec allows for ES6 Web Workers, no browser actually supports them yet. That means we needed a way to get our workers into non-ES6 form. Thankfully, roll-up can generate AMD modules, which means we now have a build step to compile our Worker source code back into AMD and use the existing TaskProcessor to load and execute them. This build step is part of the standard build task and is called createWorkers. During development, these ""built"" workers are un-optimized so you can still debug them and read the code.

Since there is a build step, that means if you are changing code that affects a worker, you need to re-run build, or you can use the build-watch task to do it automatically.

The ES6 versions of Worker code has moved into Source/WorkersES6 and we build the workers into their ""old home"" of Source/Workers. cesiumWorkerBootstrapper and transferTypedArrayTest which were already non-AMD ES5 scripts remain living in the Workers directory.

Surprisingly little was changed about TaskProcessor or the worker system in general, especially considering that I thought this would be one of the major hurdles.

ThirdParty
A lot of our ThirdParty either already had a hand-written wrapper for AMD (which I updated to ES6) or had UMD which created problems when importing the same code in both Node and the browser. I basically had to update the wrapper of every third-party library to fix these problems. In some cases I updated the library version itself (Autolinker, topojson). Nothing to be too concerned about, but future clean-up would be using npm versions of these libraries and auto-generating the wrappers as needed so we don't hand-edit things.

Sandcastle
Sandcastle is eternal and manages to live another day in it's ancient requirejs/dojo 1.x form. Sandcastle now automatically uses the ES6 version of Cesium if it is available and fallsback to the ES5 unminified version if it is now. The built version of Sandcastle always uses CesiumUnminified, just like master. This means Sandcastle still works in IE11 if you run the combine step first (or use the relase zip)

Removed Cesium usage from Sandcastle proper, since it wasn't really needed
Generate a VERSION propertyin the gallery index since Cesium is no longer being included.
Remove requirejs from Sandcastle bucket
Update bucket to use the built version of Cesium if it is available by fallbackto the ES6 version during development.
Standalone.html was also updated
There's a bit of room for further clean-up here, but I think this gets us into master. I did not rename bucket-requirejs.html because I'm pretty sure it would break previously shared demos. We can put in some backwards compatible code later on if we want. (But I'd rather just see a full Sandcastle rewrite).

Specs
Specs are now all ES6, except for TestWorkers, which remain standard JS worker modules. This means you can no longer run the unbuilt unit tests in IE11. No changes for Chrome and Firefox.

Since the specs use ES6 modules and built Cesium is an ES5 UMD, I added a build-specs build step which generates a combined ES5 version of the specs which rely on Cesium as a global variable. We then inject these files into jasmine instead of the standard specs and everything works exactly as it did before. SpecRunner.html has been updated to inject the correct version of the script depending on the build/release query parameters.

The Specs must always use Cesium by importing Source/Cesium.js, this is so we can replace it with the built Cesium as describe above.

There's a bunch of room for clean-up here, such as unifying our two copies of jasmine into a single helper file, but I didn't want to start doing that clean-up as part of this already overly big PR. The important thing is that we can still test the built version and still test on IE/Edge as needed.

I also found and fixed two bugs that were causing failing unit tests, one in BingMapsImageryProviderSpec.js (which was overwriting createImage andnot setting it back) and ShadowVolumeAppearance.js (which had a module level caching bug). I think these may have been the cause of random CI failures in master as well, but only time will tell.

For coverage, we had to switch to karma-coverage-istanbul-instrumenter for native ES6 support, but that's it.

Finally, I updated appveryor to build Cesium and run the built tests under IE. We still don't fail the build for IE, but we should probably fix that if we want to keep it going.

NodeJS
When NODE_ENV is production, we now require in the minified CesiumJS directly, which works great because it's now a UMD module. Otherwise, we use the excellant esmpackage to load individual modules, it was a fairly straightforward swap from our old requirejs usage. We could probably drop esm too if we don't care about debugging or if we provie source maps at some point.
"
""".lower()

    print("is_abstraction", is_abstraction(text))
    valid_num = len(re.findall(build_core_abstraction_regex(), text))
    print(re.findall(build_core_abstraction_regex(), text))

