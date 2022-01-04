
We classify text for Self Admitted Technical Debt (SATD).
According to wikipedia: "Technical debt (also known as design debt or code debt, but can be also related to other technical endeavors)
 is a concept in software development that reflects the implied cost of 
additional rework caused by choosing an easy (limited) solution now instead of using a better approach that would take longer".
Self admitted technical debt is a case in which the developer admits that a given code contains technical debt.

<b>Instructions</b>


  1. Classical terms for SATD (e.g., 'TODO', 'FIXME', 'HACK', 'XXX') are SATD (unless context is implies otherwise).
  1. Implicit reference to cost (e.g., "this is a workaround") is SATD.
  1. Removal of SATD is not SATD.
  1. Implementing a SATD comment is not SATD (since it removes the technical debt).
  1. Updating TODO comment is SATD
  1. Referring to general TODO lists (e.g., "Update TODO") is not SATD. Adding a specific TODO is SATD.
  1. Technical debt in documentation is SATD. 
  1. "Work in progress(WIP)" is not considered as SATD since it is uncompleted work, not low-quality work.
  1. A temporary change is considered SATD since it commits to a new future change.
  1. Bug fixed are not considered as SATD. Bugs, in general, are a problem in the solution and not a not optimal solution.
  Also, bugs are admitted when fixed, hence this is a removal of the problem, not its introduction.
  