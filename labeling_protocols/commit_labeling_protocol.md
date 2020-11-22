

    
    Commit labeling protocol




We base our taxonomy on the taxonomy of
[“Characteristics of Application Software Maintenance”](https://www.semanticscholar.org/paper/Characteristics-of-application-software-maintenance-Lientz-Swanson/2821ee262ee92a8c5c5bb90cda7d0702e9f61af5?p2df)
The main difference in taxonomy is that we add a refactoring as a sub-category inside perfective.
Other than that, we provide detailed protocols referring to cases that are usualy not considered by the high level definition.

We divide commits into

  1. Corrective - <a href="corrective_protocol.html">bug fixes</a>.
  1. Adaptive - <a href="adaptive_protocol.html">implementation of new features</a>.
  1. Perfective - <a href="perfective_protocol.html">improvement of current system with out changing its functionality. Typically documentation or refactoring</a>
  1. Refactor - <a href="refactor_protocol.html">improvement of system design without changing its functionality (part of perfective)</a>
  1. Other - whatever not fall into the above. Should be a small category




Task

Our goal is to label git commit message and decide on its type.
A commit might have several types (e.g., corrective and refactor), hence each labeling protocol and label should be followed independently.


For each commit we should following fields:

  1. Is_Corrective, taking the values, True, False and ? (as intermediate value)
  1. Is_Adaptive, taking the values, True, False and ? (as intermediate value)
  1. Is_Perfective, taking the values, True, False and ? (as intermediate value)
  1. Is_Refactor, taking the values, True, False and ? (as intermediate value)
  1. Justification which is the reason based on the text for the classification.
  1. Certain, mark cases in which the annotator is not sure in the label
  1. Comment, free text adding more information





The labeling is based on the commit message for each commit.
Ideally this will be enough for the classification.
If needed, the commit content, linked ticket and other data can be used for finding the commit type.



Instructions


  1. We consider only commit messages in English.
  1. In case of messages not in English, the comment should be “Not in English”.
  1. Unless we find an indication to a type, the default should be False.
  1. In case of uncertainty, the commit should be labeled by the option you consider most likely.
      Mark “Certain” as False and then describe the source of the uncertainty and the reasons to your decision in the comment.
  1. In case that it is hard to decide based on the commit message alone, one should check the commit content in git.
      The concept that we label is “Is the commit of the type?” and not “Does the commit message indicates the type”.
      Hence, if a fix indication is found in git, the commit should be labeled as True.
  1. The “Justification” field should contain the reason to the labeling, usuelly part of the commit message.
  1. In case of an other action, the justification should be “other action”
  1. In case of English text but no a specific term indicating a bug, the comment should be “No syntactic evidence”.
      This cases are rare. Consider text like “The previous implementation of the multiplication function returned 5 for mult(2,2).
      Now it returns 4.” The commit should be labeled as True since it is a fix, though some methods cannot identify it.
  1. Merge is a technical instrument.
      Its usage alone is not an indication regarding the content or being a bug fix. A merge commit should be judged by its content.





