# commit-classification
 
Provide languge models for commit classification, data sets and protocols.

Part of the supplementary Materials of the ["The Corrective Commit Probability Code Quality Metric"](https://arxiv.org/abs/2007.10912) paper by Idan Amit and [Dror G. Feitelson](https://www.cs.huji.ac.il/~feit/).

Please cite as
``` 
@misc{amit2020corrective,
    title={The Corrective Commit Probability Code Quality Metric},
    author={Idan Amit and Dror G. Feitelson},
    year={2020},
    eprint={2007.10912},
    archivePrefix={arXiv},
    primaryClass={cs.SE}
}
```

And the supplementary Materials of the ["Which Refactoring Reduces Bug Rate?"](http://www.cs.huji.ac.il/~feit/papers/Refactor19PROMISE.pdf) paper by Idan Amit and [Dror G. Feitelson](https://www.cs.huji.ac.il/~feit/). Promise 2019

Please cite as
``` 

@inproceedings{Amit:2019:RRB:3345629.3345631,
 author = {Amit, Idan and Feitelson, Dror G.},
 title = {Which Refactoring Reduces Bug Rate?},
 booktitle = {Proceedings of the Fifteenth International Conference on Predictive Models and Data Analytics in Software Engineering},
 series = {PROMISE'19},
 year = {2019},
 isbn = {978-1-4503-7233-6},
 location = {Recife, Brazil},
 pages = {12--15},
 numpages = {4},
 url = {http://doi.acm.org/10.1145/3345629.3345631},
 doi = {10.1145/3345629.3345631},
 acmid = {3345631},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Code quality, machine learning, refactoring},
} 
```

See here the [analysis utilities](https://github.com/evidencebp/analysis_utils)

See here the [corrective commit probability code](https://github.com/evidencebp/corrective-commit-probability)

# Project structure

## [Labeling Protocols](https://github.com/evidencebp/commit-classification/tree/master/labeling_protocols)
There are many nuances in the definition of concepts.Should a typo be considered a bug fix?What about bugs in test files?
We defined protocols that prosent the guidelines with respect to them we label.That makes the decision taken transparent and helps researchers considering a dataset to decide if it fits their needs.

## [Data sets](https://github.com/evidencebp/commit-classification/tree/master/data)

This directory contains manually labeled data sets for the classifiers.The samples are labeled by the protocol.The sampling column, when exists, references the query used to sample them.This is important since random sampling, a sample of hits and active learning sampling have different properties and usage.
