"""
    Implements a confusion matrix.
    For details see https://en.wikipedia.org/wiki/Confusion_matrix
"""


def ifnull(var, val=0):
  if var is None:
    return val

  return var

def safe_divide(numerator, divisor, default=None):
    if divisor != 0 and divisor is not None:
        return ifnull(numerator)/ifnull(divisor)
    else:
        return default

class ConfusionMatrix(object):
    def __init__(self
                 , classifier
                 , concept
                 , count
                 , g_df=None
                 , comment=None
                 , digits=2):

        self.classifier = classifier
        self.concept = concept
        self.count = count
        self.comment = comment
        self.digits = digits

        # The be extended to enable many initialzations
        # Using a raw dataframe, sk-learn parameters, confusion matrix values
        if g_df is not None:
            self.g_df = g_df

    def tp(self):
        """
            Return True Positives (TP)
        """
        tp = 0
        if  len(self.g_df[(self.g_df[self.classifier] == True) & (self.g_df[self.concept] == True)]) == 1:
            tp = self.g_df[(self.g_df[self.classifier] == True)
                           & (self.g_df[self.concept] == True)].iloc[0][self.count]

        return tp

    def tn(self):
        """
            Return True Negatives (TN)
        """
        tn = 0
        if  len(self.g_df[(self.g_df[self.classifier] == False) & (self.g_df[self.concept] == False)]) == 1:
            tn = self.g_df[(self.g_df[self.classifier] == False)
                           & (self.g_df[self.concept] == False)].iloc[0][self.count]

        return tn

    def fp(self):
        """
            Return False Positives (FP)
        """
        fp = 0
        if  len(self.g_df[(self.g_df[self.classifier] == True) & (self.g_df[self.concept] == False)]) == 1:
            fp = self.g_df[(self.g_df[self.classifier] == True)
                           & (self.g_df[self.concept] == False)].iloc[0][self.count]

        return fp

    def fn(self):
        """
            Return False Negatives (FN)
        """
        fn = 0
        if  len(self.g_df[(self.g_df[self.classifier] == False) & (self.g_df[self.concept] == True)]) == 1:
            fn = self.g_df[(self.g_df[self.classifier] == False)
                           & (self.g_df[self.concept] == True)].iloc[0][self.count]

        return fn

    def positives(self):
        return (ifnull(self.tp()) + ifnull(self.fn()))

    def positive_rate(self):
        return safe_divide(self.positives(), self.samples())

    def negatives(self):
        return (ifnull(self.tn()) + ifnull(self.fp()))

    def hits(self):
        return (ifnull(self.tp()) + ifnull(self.fp()))

    def hit_rate(self):
        return safe_divide(self.hits(), self.samples())

    def precision(self):
        return safe_divide(self.tp(), self.hits())

    def precision_lift(self):
        return ifnull(safe_divide(ifnull(self.precision()), self.positive_rate())) - 1.0

    def recall(self):
        return safe_divide(self.tp(), self.positives())

    def samples(self):
        return self.positives() + self.negatives()

    def accuracy(self):
        return safe_divide(self.tp() + self.tn(), self.samples())

    def fpr(self):
        """
            False Positive Rate
        :return:
        """
        return safe_divide(self.fp() , self.negatives())

    def jaccard(self):
        return safe_divide(self.tp() , self.tp() + self.fp() + self.fn())
    # TODO  - confusion matix metrics

    def summarize(self):

        return {'true_positives' : self.tp()
                , 'true_negatives' : self.tn()
                , 'false_positives' : self.fp()
                , 'false_negatives' : self.fn()
                , 'samples' : self.samples()
                , 'accuracy' : round(ifnull(self.accuracy()), self.digits)
                , 'positive_rate' : round(ifnull(self.positive_rate()), self.digits)
                , 'hit_rate' : round(ifnull(self.hit_rate()), self.digits)
                , 'precision' : round(ifnull(self.precision()), self.digits)
                , 'precision_lift' : round(ifnull(self.precision_lift()), self.digits)
                , 'recall' : round(ifnull(self.recall()), self.digits)
                , 'fpr' : round(ifnull(self.fpr()), self.digits)
                , 'jaccard' : round(ifnull(self.jaccard()), self.digits)
                , 'comment' : self.comment
                }


    def to_latex(self
                 , caption):

        print(r"\begin {table}[h!]\centering")
        print(r"\caption{", caption, "}")
        print(r"\begin {tabular} { | l | l | l |}")
        print(r"\hline")
        print(r"		&\multicolumn{2}{c|}{Classification}		  \\ \cline{2-3}")
        print(r"Concept & True(Corrective) & False              \\ \hline")
        print(r"True & ", self.tp(), "(", round(100*self.tp()/self.samples(), self.digits) ,"\% ) TP")
        print(r"& ", self.fn(), "(", round(100*self.fn()/self.samples(), self.digits) ,r"\% ) FN      \\ \hline")
        print(r"False & ", self.fp(), "(" , round(100*self.fp()/self.samples(), self.digits) ,r"\% ) FP")
        print(r"& ", self.tn(),  "(" , round(100*self.tn()/self.samples(), self.digits) ,r"\% ) TN \\ \hline")
        print(r"\end {tabular}")
        print(r"\end {table}")
