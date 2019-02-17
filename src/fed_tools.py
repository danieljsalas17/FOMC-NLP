# Author: Daniel Salas
# Created: Feb 17, 2019
# Updated: Feb 17, 2019
# ----------------------------------------------------------------------------
# fed_tools is a module that contains functions, classes, and other useful
# tools that I use often on this Fed-NLP-Scrape project.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA, NMF
import Stemmer
plt.style.use('ggplot')

# better TfidfVectorizer
english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: english_stemmer.stemWords(analyzer(doc))

# dataframe builder
def get_sample_df(dependent_vars=None,tfidf=False):
    '''Returns a pandas dataframe based of the sample FOMC statements
    -----
    INPUT
    -----
    dependent_vars: list, dict, Default = None
        - adds a column in the dataframe for the dependent variables of choice.
        Options: '3m' (3 month T-Bill rates), '10y' (10 year T-Bill rates),
        'ycurve' (slope of yield curve), 'fedfunds' (Fed Funds Rate),
        'sp500' (S&P 500 index).

        If a specified number of lags is desired, then pass in a dict where
        the dep_var strings are keys and the values are tuples such that
        (backward_lags,forward_lags). Example:
            {'3m': (2,1),
            'sp500': (0,3)}
         3m T-bill column is added along with a column for both of 2 days before
         and 1 day after. S&P 500 data along with columns for all 3 days after.
    tfidf: bool or TfidfVectorizer, Default = False
        - False leaves the text data as is. True applies the default tfidf
        methods within this module. If a custom TfidfVectorizer is passed in,
        then the custom one is used.
    ------
    OUTPUT
    ------
    df: pandas.DataFrame object
    '''
    # read data into dataframe
    df = pd.read_json('~/Projects/Fed-NLP-Scrape/data/fed_sample_statements.json')
    df.sort_index(inplace=True)
    df.rename({'data':'date'},axis='columns')
    df.date = pd.to_datetime(df.date)

    # add dependent variables
    if type(dependent_vars)==type(''):
        add_dependent_var(df,dep_var)
    elif: type(dependent_vars)==type(['','']):
        for dep_var in dependent_vars:
            add_dependent_var(df,dep_var)
    elif: type(dependent_vars)==type({'': (1,1)}):
        for dep_var,lags in dependent_vars.items():
            add_dependent_var(df,dep_var,back_lags=lags[0],fwd_lags=lags[1])
    # convert text data to tfidf
    if (type(tfidf)==type(True)):
        if tfidf:
            # IMPLEMENT THIS: default TfidfVectorizer
            tfidf=1
    else:
        # custom TfidfVectorizer
        tfidf =1
    return df

# Dependent Variables Dataset Names
dep_var_data = {'3m':'T-bill_3m.csv',
                '10y':'T-bill_10y.csv',
                'fedfunds':'fedfunds.csv',
                'sp500':'sp500_dailyclose.csv'}

def add_dependent_var(df,dep_var,back_lags=0,fwd_lags=0):
    '''Adds dependent variable to an existing pandas dataframe (df)
    -----
    INPUT
    -----
    df: pandas.DataFrame object
        - df must have a column named 'date' with datetime references, so this
        function can add the correct time series variables
    dep_var: string
        - dependend variable of interest: '3m' (3 month T-Bill rates), '10y' (10 year T-Bill rates),
        'ycurve' (slope of yield curve), 'fedfunds' (Fed Funds Rate),
        'sp500' (S&P 500 index)
    back_lags: int >= 0
        - lagged dependent variables. Adds additional column for the value of
        the depenedent variable the days before each date.
    fwd_lags: int >= 0
        - forward lagged dependent variables. Adds columns for the value of the
        dependent variable after the specified date.
    ------
    OUTPUT
    ------
    df: pandas.DataFrame
        - contains new columns with dep var data
    '''
    # implement date functions so that correct data is added
    pass
