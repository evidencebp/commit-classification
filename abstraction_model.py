# Design patterns list is based on wikipedia https://en.wikipedia.org/wiki/Software_design_pattern
import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX, VERB_E_SUFFIX, NEAR_ENOUGH\
 , programming_languges, software_goals
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

"""
interface, encapsulation, composition, coupling, single responsibility, Liskov, virtual method, design, design patterns
, inheritance, Structured programming, ADT (abstract data type),  polymorphism, delegation, template, generic, object oriented
, Refinement, Reification
, liskov substitution principle
, solid, dry principle, composition, reuse
"""
core_abstraction_terms = [
'abstraction',
'abtract'  + REGULAR_SUFFIX,
'adapter(?:s)?',
'adt',# Abstract Data Type
'bridge(?:s)?',
'chain of responsibility',
'composite',
'compos' + VERB_E_SUFFIX,
'composition',
'coupl'  + VERB_E_SUFFIX,
'controler(?:s)?',
'de(?: |-)?compos'  + VERB_E_SUFFIX,
'de(?: |-)?composition',
'de(?: |-)?coupl'  + VERB_E_SUFFIX,
'decorator(?:s)?',
'delegat' + VERB_E_SUFFIX,
'delegation',
'dependenc(?:y|ies)',
'dependency injection',
'dependency inversion',
'design',
'design(?: |-)pattern(?:s)?',
'dry principle', # Don't Repeat Yourself
'encapsulat' + VERB_E_SUFFIX,
'encapsulation',
'facade(?:s)?',
'factory',
'flyweight(?:s)?',
'generic(?:s)?',
'inheritance',
'interface',
'interface segregation',
'iterator(?:s)?',
'lazy initialization',
'liskov', # Liskov substitution principle
'marker(?:s)?',
'mediator',
'memento',
'multiton',
'object(?:s)?(?: |-)pool(?:s)?',
'observer(?:s)?',
'object(?: |-)oriented',
'open(?: |-)closed principle',
'polymorphism',
'prototype(?:s)?',
'prox(?:y|ies)',
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
'specification(?:s)?', # consider
'state(?:s)?', # consider
'strateg(?:y|ies)',
'sub(?:-| )?class(?:es)?',
'super(?:-| )?class(?:es)?',
'template(?:s)?',
'twins(?:s)?',
'translator(?:s)?',
'virtual method',
'visitor(?:s)?',
'wrapper(?:s)?',

] + software_goals



excluded_abstraction_terms = ['reduc(es|e|ed|ing) abstraction', '(useless|bad) abstraction']

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
    print_abstractionfunctions_for_bq(commit='951c76e61b73b6afdcdb8a8d2b1ec5f268526c3b')
    #evaluate_cc_fix_classifier()

    text = """
"Standardized the JS calling convention
https://bugs.webkit.org/show_bug.cgi?id=72221
        
Reviewed by Oliver Hunt.

This patch standardizes the calling convention so that the caller always
sets up the callee's CallFrame. Adjustments for call type, callee type,
argument count, etc. now always take place after that initial setup.
        
This is a step toward reversing the argument order, but also has these
immediate benefits (measured on x64):
        
(1) 1% benchmark speedup across the board.
        
(2) 50% code size reduction in baseline JIT function calls.
        
(3) 1.5x speedup for single-dispatch .apply forwarding.
        
(4) 1.1x speedup for multi-dispatch .apply forwarding.

This change affected the baseline JIT most, since the baseline JIT had
lots of ad hoc calling conventions for different caller / callee types.

* assembler/MacroAssemblerX86_64.h:
(JSC::MacroAssemblerX86_64::branchPtr):
(JSC::MacroAssemblerX86_64::branchAddPtr): Optimize compare to 0 into
a test, like other assemblers do. (I added some compares to 0, and didn't
want them to be slow.)

* bytecode/CodeBlock.cpp:
(JSC::CodeBlock::dump): Merged op_load_varargs into op_call_varargs so
op_call_varargs could share code generation with other forms of op_call.
This is also a small optimization, since op_*varargs no longer have to
pass arguments to each other through the register file.

(JSC::CallLinkInfo::unlink):
* bytecode/CodeBlock.h: Added a new call type: CallVarargs. This allows
us to link functions called through .apply syntax. We need to distinguish
CallVarargs from Call because CallVarargs changes its argument count
on each inovcation, so we must always link to the argument count checking
version of the callee.

* bytecode/Opcode.h:
* bytecompiler/BytecodeGenerator.cpp:
(JSC::BytecodeGenerator::emitCallVarargs):
* bytecompiler/BytecodeGenerator.h: Merged op_load_varargs into op_call_varargs.

* bytecompiler/NodesCodegen.cpp:
(JSC::ApplyFunctionCallDotNode::emitBytecode): Ditto. Also, simplified
some of this bytecode generation to remove redundant copies.

* dfg/DFGJITCodeGenerator32_64.cpp:
(JSC::DFG::JITCodeGenerator::emitCall):
* dfg/DFGJITCodeGenerator64.cpp:
(JSC::DFG::JITCodeGenerator::emitCall): Added a new call type: CallVarargs.
DFG doesn't support this type, but its code needs to change slightly
to accomodate a 3-state variable.

Stopped passing the argument count in regT1 because this is non-standard.
(The argument count goes in the CallFrame. This trades speed on the slow
path for speed and code size on the fast path, and simplicity on all paths.
A good trade, in my opinion.)

* dfg/DFGJITCompiler.cpp:
(JSC::DFG::JITCompiler::compileEntry):
(JSC::DFG::JITCompiler::link):
(JSC::DFG::JITCompiler::compile):
(JSC::DFG::JITCompiler::compileFunction): Tweaked code to make CallFrame
setup more obvious when single-stepping. Also, updated for argument count
not being in regT1.

* dfg/DFGJITCompiler.h:
(JSC::DFG::JITCompiler::addJSCall):
(JSC::DFG::JITCompiler::JSCallRecord::JSCallRecord): Added a new call
type: CallVarargs.

* dfg/DFGOperations.cpp: Do finish CallFrame setup in one place before
doing anything else. Don't check for stack overflow because we have no callee
registers, and our caller has already checked for its own registers.

* dfg/DFGRepatch.cpp:
(JSC::DFG::dfgLinkFor): We can link to our callee even if our argument
count doesn't match -- we just need to link to the argument count checking
version.

* interpreter/CallFrameClosure.h:
(JSC::CallFrameClosure::setArgument): BUG FIX: When supplying too many
arguments from C++, we need to supply a full copy of the arguments prior
to the subset copy that matches our callee's argument count. (That is what
the standard calling convention would have produced in JS.) I would have
split this into its own patch, but I couldn't find a way to get the JIT
to fail a regression test in this area without my patch applied.

* interpreter/Interpreter.cpp: Let the true code bomb begin!

(JSC::eval): Fixed up this helper function to operate on eval()'s CallFrame,
and not eval()'s caller frame. We no longer leave the CallFrame pointing
to eval()'s caller during a call to eval(), since that is not standard.

(JSC::loadVarargs): Factored out a shared helper function for use by JIT
and interpreter because half the code means one quarter the bugs -- in my
programming, at least.

(JSC::Interpreter::execute): Removed a now-unused way to invoke eval.
        
(JSC::Interpreter::privateExecute): Removed an invalid ASSERT following
putDirect, because it got in the way of my testing. (When putting a
function, the cached base of a PutPropertySlot can be 0 to signify ""do
not optimize"".)
        
op_call_eval: Updated for new, standard eval calling convention.
        
op_load_varargs: Merged op_load_varargs into op_call_varargs.

op_call_varags: Updated for new, standard eval calling convention. Don't
check for stack overflow because the loadVarargs helper function already
checked.

* interpreter/Interpreter.h:
(JSC::Interpreter::execute): Headers are fun and educational!

* interpreter/RegisterFile.cpp:
(JSC::RegisterFile::growSlowCase):
* interpreter/RegisterFile.h:
(JSC::RegisterFile::grow): Factored out the slow case into a slow
case because it was cramping the style of my fast case.

* jit/JIT.cpp:
(JSC::JIT::privateCompile): Moved initialization of
RegisterFile::CodeBlock to make it more obvious when debugging. Removed
assumption that argument count is in regT1, as above. Removed call to
restoreArgumentReference() because the JITStubCall abstraction does this for us.

(JSC::JIT::linkFor): Link even if we miss on argument count, as above.

* jit/JIT.h:
* jit/JITCall32_64.cpp:
(JSC::JIT::emitSlow_op_call):
(JSC::JIT::emitSlow_op_call_eval):
(JSC::JIT::emitSlow_op_call_varargs):
(JSC::JIT::emitSlow_op_construct):
(JSC::JIT::emit_op_call_eval):
(JSC::JIT::emit_op_call_varargs): Share all function call code generation.
Don't count call_eval when accounting for linkable function calls because
eval doesn't link. (Its fast path is to perform the eval.)

(JSC::JIT::compileLoadVarargs): Ported this inline copying optimization
to our new calling convention. The key to this optimization is the
observation that, in a function that declares no arguments, if any
arguments are passed, they all end up right behind 'this'.

(JSC::JIT::compileCallEval):
(JSC::JIT::compileCallEvalSlowCase): Factored out eval for a little clarity.

(JSC::JIT::compileOpCall):
(JSC::JIT::compileOpCallSlowCase): If you are still with me, dear reader,
this is the whole point of my patch. The caller now unconditionally moves
the CallFrame forward and fills in the data it knows before taking any
branches to deal with weird caller/callee pairs.
        
This also means that there is almost no slow path for calls -- it all
gets folded into the shared virtual call stub. The only things remaining
in the slow path are the rare case counter and a call to the stub.

* jit/JITOpcodes32_64.cpp:
(JSC::JIT::privateCompileCTIMachineTrampolines):
(JSC::JIT::privateCompileCTINativeCall): Updated for values being in
different registers or in memory, based on our new standard calling
convention.
        
Added a shared path for calling out to CTI helper functions for non-JS
calls.

* jit/JITPropertyAccess32_64.cpp:
(JSC::JIT::emit_op_method_check): method_check emits its own code and
the following get_by_id's code, so it needs to add both when informing
result chaining of its result. This is important because the standard
calling convention can now take advantage of this chaining.

* jit/JITCall.cpp:
(JSC::JIT::compileLoadVarargs):
(JSC::JIT::compileCallEval):
(JSC::JIT::compileCallEvalSlowCase):
(JSC::JIT::compileOpCall):
(JSC::JIT::compileOpCallSlowCase):
* jit/JITOpcodes.cpp:
(JSC::JIT::privateCompileCTIMachineTrampolines):
(JSC::JIT::emit_op_call_eval):
(JSC::JIT::emit_op_call_varargs):
(JSC::JIT::emitSlow_op_call):
(JSC::JIT::emitSlow_op_call_eval):
(JSC::JIT::emitSlow_op_call_varargs):
(JSC::JIT::emitSlow_op_construct): Observe, as I write all of my code a
second time, now with 64 bits.

* jit/JITStubs.cpp:
(JSC::throwExceptionFromOpCall):
(JSC::jitCompileFor):
(JSC::arityCheckFor):
(JSC::lazyLinkFor): A lot of mechanical changes here for one purpose:
Exceptions thrown in the middle of a function call now use a shared helper
function (throwExceptionFromOpCall). This function understands that the
CallFrame currently points to the callEE, and the exception must be
thrown by the callER. (The old calling convention would often still have
the CallFrame pointing at the callER at the point of an exception. That
is not the way of our new, standard calling convention.)

(JSC::op_call_eval): Finish standard CallFrame setup before calling 
our eval helper function, which now depends on that setup.

* runtime/Arguments.h:
(JSC::Arguments::length): Renamed numProvidedArguments() to length()
because that's what other objects call it, and the difference made our
new loadVarargs helper function hard to read.

* runtime/Executable.cpp:
(JSC::FunctionExecutable::compileForCallInternal):
(JSC::FunctionExecutable::compileForConstructInternal): Interpreter build
fixes.

* runtime/FunctionPrototype.cpp:
(JSC::functionProtoFuncApply): Honor Arguments::MaxArguments even when
the .apply call_varargs optimization fails. (This bug appears on layout
tests when you disable the optimization.)


git-svn-id: bf5cd6ccde378db821296732a091cfbcf5285fbd@100165 bbb929c8-8fbe-4397-9dbb-9b2b20218538"
    """.lower()

    print("is_abstraction", is_abstraction(text))
    valid_num = len(re.findall(build_core_abstraction_regex(), text))
    print(re.findall(build_core_abstraction_regex(), text))

