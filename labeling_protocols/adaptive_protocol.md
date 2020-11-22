
    
    Adaptive labeling protocol



Task

Our goal is to label git commit message and decide whether the commit is adaptive, adding a new feature.

For each commit we should fill these fields:

  1. Is_adaptive, taking the values, True, False and ? (as intermediate value).
  1. Justification which is the reason based on the text for the classification.
  1. Comment, any unstructured information of interest.
  1. certain, default True, change to false when not sure in the classification.


The labeling is based on the commit message for each commit.
Ideally this will be enough for the classification.
If needed, the commit content, linked ticket and other data can be used for finding the commit type.


Instructions


  1. We consider only commit messages in English.
  1. Unless we find an indication to a adpative contant, the default should be False.
  1. In case of uncertainty, the commit should be labeled by the option you consider most likely. Start the justification with the word “Uncertain” and then describe the source of the uncertainty and the reasons to your decision.
  1. In case that it is hard to decide based on the commit message alone, one should check the commit content in git. The concept that we label is “Is the commit a adaptaive?” and not “Does the commit message indicates an adaptive work”.
    Hence, if an adaptive indication is found in git, the commit should be labeled as True.
  1. The “Justification” field should contain the reason to the labeling.
  1. In case of a specific common non adaptive action (e.g., bug fix, refactor, performance improvement), the action should be named.
  1. In case of an other action, the justification should be “other action”
  1. In case of an adaptive, the justification should be support from the text (e.g., Added, Changed).
  1. In case of messages not in English, the comment should be “Not in English”.
  1. In case of English text but no a specific term indicating an adaptive, the comment should be “No syntactic evidence”. This cases are rare.

  1. Adding a new feature is adaptive.
  1. Changing a feature is adaptive.
  1. Changing a feature implementation yet keeping its functionality is a refactor, not adaptive.
  1. Removing a feature is adaptive.
  1. Performance improvement is adaptive.
  1. Removing dead code is a refactor, not adaptive.
  1. Code review fixes is adaptive
  1. Fixing (merge) conflicts is adaptive
  1. Fixing static analysis warning, which are not bugs, is adaptive
  1. Upgrading a library, is adaptive
  1. Bumping self version is perfective, not adaptive

  1. Debug message/ feature aimed not to the end user - adaptive. We consider the features for programmers as part of the features.
  1. Changing an interface is adaptive.
  1. Updating a library is adaptive
  1. Porting code is adaptive

  1. Tests are considered to be a part of the system and its requirements. Therefore, an adaptive change in the tests is adaptive and should be labeled as True.
  1. Merge is a technical instrument. It is adaptive since it modifies the system. A merge commit might have more functions judged by its content.
      Since merge commits can be identified by having more than a single parent, it is easy to be flexible in their usage.
  
  1. While our rule is to find a positive indication to the commit type, some messages like 'WIP' has no indication.
      We handle them by identifying the specific cases in a detected rule and mark them as adaptive as the most reasonable default.
  
  1.  When <a href="https://www.conventionalcommits.org/">conventional commits</a> appear, we base the decision upon them.
    The labels 'feat', 'build', 'chore', 'ci', 'test', and 'perf' are adaptive.




