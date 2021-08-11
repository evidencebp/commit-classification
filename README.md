# commit-classification
 
Provide languge models for commit classification, data sets and protocols.

# Corrective commit probability: a measure of the effort invested in bug fixing
Supplementary Materials of the ["Corrective commit probability: a measure of the effort invested in bug fixing"](https://www.cs.huji.ac.il/~feit/papers/CCP21SQJ.pdf) paper by Idan Amit and [Dror G. Feitelson](https://www.cs.huji.ac.il/~feit/).

Please cite as
``` 
@Article{Amit2021CCP,
author={Amit, Idan
and Feitelson, Dror G.},
title={Corrective commit probability: a measure of the effort invested in bug fixing},
journal={Software Quality Journal},
year={2021},
month={Aug},
day={05},
abstract={The effort invested in software development should ideally be devoted to the implementation of new features. But some of the effort is invariably also invested in corrective maintenance, that is in fixing bugs. Not much is known about what fraction of software development work is devoted to bug fixing, and what factors affect this fraction. We suggest the Corrective Commit Probability (CCP), which measures the probability that a commit reflects corrective maintenance, as an estimate of the relative effort invested in fixing bugs. We identify corrective commits by applying a linguistic model to the commit messages, achieving an accuracy of 93{\%}, higher than any previously reported model. We compute the CCP of all large active GitHub projects (7,557 projects with 200+ commits in 2019). This leads to the creation of an investment scale, suggesting that the bottom 10{\%} of projects spend less than 6{\%} of their total effort on bug fixing, while the top 10{\%} of projects spend at least 39{\%} of their effort on bug fixing --- more than 6 times more. Being a process metric, CCP is conditionally independent of source code metrics, enabling their evaluation and investigation. Analysis of project attributes shows that lower CCP (that is, lower relative investment in bug fixing) is associated with smaller files, lower coupling, use of languages like JavaScript and C{\#} as opposed to PHP and C++, fewer code smells, lower project age, better perceived quality, fewer developers, lower developer churn, better onboarding, and better productivity.},
issn={1573-1367},
doi={10.1007/s11219-021-09564-z},
url={https://doi.org/10.1007/s11219-021-09564-z},
pages={1--45},
publisher={Springer}

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

# Project structure

## [Labeling Protocols](https://github.com/evidencebp/commit-classification/tree/master/labeling_protocols)
There are many nuances in the definition of concepts.Should a typo be considered a bug fix?What about bugs in test files?
We defined protocols that prosent the guidelines with respect to them we label.That makes the decision taken transparent and helps researchers considering a dataset to decide if it fits their needs.

## [Data sets](https://github.com/evidencebp/commit-classification/tree/master/data)

This directory contains manually labeled data sets for the classifiers.The samples are labeled by the protocol.The sampling column, when exists, references the query used to sample them.This is important since random sampling, a sample of hits and active learning sampling have different properties and usage.

## [Queries](https://github.com/evidencebp/commit-classification/tree/master/queries)

Our main data source is [BigQuery GitHub scheme](https://console.cloud.google.com/bigquery?d=github_repos&p=bigquery-public-data&page=dataset) and the [research infrostructure](https://github.com/evidencebp/general) we built upon it. The queries directory contains queries for sampling the data set and big query functions (generated from the Python models and used on BigQuery).

## Main directory

Python code that builds each of the models.
Our models are aimed to run on Bigquery and therefore should be implemented using regular expression.
The Python code is used for decomposition and reuse and makes the code more concise.


## [Resources](https://github.com/evidencebp/commit-classification/blob/master/resources.md)
There is plenty of great work in the field.Data sets are being created, language constructs are published.We collect here links that can be useful for linguistic analysis in software engineering.If you are familiar with such resources, please inform us.

## Related repositories

See here the [research infrostructure](https://github.com/evidencebp/general) constructing our software engineering scheme

See here the [analysis utilities](https://github.com/evidencebp/analysis_utils)


See here the [corrective commit probability code](https://github.com/evidencebp/corrective-commit-probability), using all the above

# Versions

Version used for "ComSum: Commit Messages Summarization and Meaning Preservation" by Leshem Choshen and Idan Amit.

[![DOI](https://zenodo.org/badge/253520268.svg)](https://zenodo.org/badge/latestdoi/253520268)

Live version is updating at https://github.com/evidencebp/commit-classification

Repository will keep advancing.
