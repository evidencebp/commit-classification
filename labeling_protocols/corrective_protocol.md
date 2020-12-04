
    
    Bug fix labeling protocol




Instructions


  1. Fixes that are not bug fixes (e.g., documentation, style) should be labeled as False.
  1. Specifically, typos and spelling errors should be labeled as False.
  1. Warning fix (e.g., pylint warning) are not considered to a bug fix and should be labeled as False.
  1. Unless the change is aimed to solve a specific known problem, it is not a fix.
      For example, in “improving reliability”, one cannot point at the problem being fixed. These cases should be labeled as False.
  1. In cases that the commit contains some modifications, if at least one of them is considered a bug fix
      , the commit should be labeled as True.
  1. Fix to build/compile, are considered a bug fix and should be labeled as True.
  1. Tests are considered to be a part of the system and its requirements.
      Therefore, a bug fix in the tests is a bug fix and should be labeled as True.
  1.  When <a href="https://www.conventionalcommits.org/">conventional commits</a> appear, we base the decision upon them.
    The label 'fix' is corrective.




