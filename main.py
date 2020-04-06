"""
The repository is mainly stateless since this is a language library
commit_type_model is a python program that decompose enitities and generate a regular experssion.
One can use them in python program.
For use in BigQuery, the file also genertae function.
The current functions are in the bq_*.sql scripts.
If one moodifes the commit_type_model, recration and redployment of the scripts is needed.

The confusion matrix is a utility for performance evaluation.
For the evaluation of the given classifiers use linguistic_model_performance that will evalute them on the
labled samples in the data directory
"""
