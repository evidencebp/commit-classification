The data file BugsInPy_Labelled.csv is from [BugsInPy: A Database of Existing Bugs in Python Programs to
Enable Controlled Testing and Debugging Studies](https://dl.acm.org/doi/pdf/10.1145/3368089.3417943)
The file BugsInPy_Labelled_text.csv contains the same commits, enhanched with the commit message and subject.

Please cite as
```
@inproceedings{10.1145/3368089.3417943,
author = {Widyasari, Ratnadira and Sim, Sheng Qin and Lok, Camellia and Qi, Haodi and Phan, Jack and Tay, Qijin and Tan, Constance and Wee, Fiona and Tan, Jodie Ethelda and Yieh, Yuheng and Goh, Brian and Thung, Ferdian and Kang, Hong Jin and Hoang, Thong and Lo, David and Ouh, Eng Lieh},
title = {BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies},
year = {2020},
isbn = {9781450370431},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3368089.3417943},
doi = {10.1145/3368089.3417943},
abstract = {The 2019 edition of Stack Overflow developer survey highlights that, for the first time, Python outperformed Java in terms of popularity. The gap between Python and Java further widened in the 2020 edition of the survey. Unfortunately, despite the rapid increase in Python's popularity, there are not many testing and debugging tools that are designed for Python. This is in stark contrast with the abundance of testing and debugging tools for Java. Thus, there is a need to push research on tools that can help Python developers. One factor that contributed to the rapid growth of Java testing and debugging tools is the availability of benchmarks. A popular benchmark is the Defects4J benchmark; its initial version contained 357 real bugs from 5 real-world Java programs. Each bug comes with a test suite that can expose the bug. Defects4J has been used by hundreds of testing and debugging studies and has helped to push the frontier of research in these directions. In this project, inspired by Defects4J, we create another benchmark database and tool that contain 493 real bugs from 17 real-world Python programs. We hope our benchmark can help catalyze future work on testing and debugging tools that work on Python programs.},
booktitle = {Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering},
pages = {1556–1560},
numpages = {5},
keywords = {Bug Database, Python, Testing and Debugging},
location = {Virtual Event, USA},
series = {ESEC/FSE 2020}
}
```

The labels are:
(1) The change involves no refactoring + new features
(2) The change may involve refactoring + new features
(3) The change for sure involves refactoring + new features (e.g., have a new file added that is not related to the buggy line)
(4) The change is not related to a bug, and only performs refactoring + new features

The BugsInPy paper investigets the commit that both authors label as (1)
