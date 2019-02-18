# Author: Daniel Salas
# Created: Feb 17, 2019
# Updated: Feb 17, 2019
# ----------------------------------------------------------------------------
# fed_tools is a module that contains functions, classes, and other useful
# tools that I use often on this Fed-NLP-Scrape project.

# TODO
##------
# * API's
    # * Look into FRED api for daily updates of data (specifically fed_funds)
    # * Look into US Treasury API (or FRED) for daily updates of T-bill rates
    # * Look into a S&P 500 data update API
    # * For now, using these:
        # * 3m: https://fred.stlouisfed.org/series/DTB3
        # * 10y: https://fred.stlouisfed.org/series/DGS10/
        # * fedfunds: https://fred.stlouisfed.org/series/DFF
        # * sp500: https://finance.yahoo.com/quote/%5EGSPC/history?period1=-630961200&period2=1550466000&interval=1d&filter=history&frequency=1d

# * optimize add_dependent_var: right now it loads the entire dataset into a
# separate dataframe and then matches on dates. Selective loading could speed it
# up, but the datasets aren't that big, so not a huge problem right now

#-------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA, NMF
import Stemmer
from datetime import datetime
from datetime import timedelta
plt.style.use('ggplot')

# All file access commands start here
directory = '~/Projects/Fed-NLP-Scrape/'

# better TfidfVectorizer
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        english_stemmer = Stemmer.Stemmer('en')
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
    df = pd.read_json(directory+'data/fed_sample_statements.json')
    df.sort_index(inplace=True)
    df.rename({'data':'date'},axis='columns',inplace=True)
    df.date = pd.to_datetime(df.date)

    # add dependent variables
    if type(dependent_vars)==type(''):
        # str case: only one dep_var added
        add_dependent_var(df,dep_var)
    elif type(dependent_vars)==type(['','']):
        # list case: at least one dep_var added
        for dep_var in dependent_vars:
            add_dependent_var(df,dep_var)
    elif type(dependent_vars)==type({'': (1,1)}):
        # dictionary case: at least one dep_var and custom lags added
        for dep_var,lags in dependent_vars.items():
            add_dependent_var(df,dep_var,back_lags=lags[0],fwd_lags=lags[1])
    # convert text data to tfidf
    if (type(tfidf)==type(True)):
        if tfidf:
            vectorizer = StemmedTfidfVectorizer(stop_words='english',
                                                strip_accents='ascii')
            # create tfidf sparse matrix
            tfidf_sparse = vectorizer.fit_transform(df.doc)

            # create column names for tfidf features
            tfidf_colnames = vectorizer.get_feature_names()
            for i,feature_name in enumerate(tfidf_colnames):
                tfidf_colnames[i] = 'tfidf_'+feature_name

            # create tfidf dataframe
            tfidf_df = pd.DataFrame(data=tfidf_sparse.toarray(),
                                    columns=tfidf_colnames)
            # concatenate tfidf dataframe to base dataframe
            df = pd.concat([df,tfidf_df],axis=1)
    else:
        # custom TfidfVectorizer
        tfidf = 1
    return df

# Dependent Variables Dataset Names
# datasets must have only 2 columns: date and val
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
    # sp500 data doesn't change on weekends, I think. Hopefully not issue
    # eventually want to speed up loading so that not whole dependent variable
    # dataset is loaded for this function.

    # load dependent variable data
    dep_df = pd.read_csv(directory+'data/'+dep_var_data[dep_var],
                         parse_dates=['date'])

    # match dep_var to df
    df.merge(dep_df,on='date')
    df.rename({'val':dep_var},axis='columns',inplace=True)

    # backward lags
    for back_lag in range(1,back_lags+1):
        dep_df.date = dep_df.date + timedelta(days=back_lag)
        df.merge(dep_df,on='date')
        df.rename({'val':dep_var+'_B{}'.format(back_lag)},inplace=True)
    # forward lags
    for fwd_lag in range(1,fwd_lags+1):
        dep_df.date = dep_df.date + timedelta(days=fwd_lag)
        df.merge(dep_df,on='date')
        df.rename({'val':dep_var+'_F{}'.format(fwd_lag)},inplace=True)

    return df

# dependent variable cleaner
def clean_dep_data():
    '''Creates a clean version of the dependent raw dependent variable data.
    The clean version is necessary to use other fed_tools with dep vars.
    '''
    # for now, this just cleans dep_var data from my local, raw files
    raw = {'3m':        {'file':'DTB3.csv',
                         'date':'DATE',
                         'val' :'DTB3'},
           '10y':       {'file':'DGS10.csv',
                         'date':'DATE',
                         'val' :'DGS10'},
           'fedfunds':  {'file':'DFF.csv',
                         'date':'DATE',
                         'val' :'DFF'},
           'sp500':     {'file':'^GSPC.csv',
                         'date':'Date',
                         'val' :'Adj Close'}}

    for key,new_file in dep_var_data.items():
        # load raw file
        df = pd.read_csv(directory+'data/'+raw[key]['file'])
        # rename columns to desired names
        df.rename({raw[key]['date']:'date',raw[key]['val']:'val'},
                  axis='columns',inplace=True)
        # save clean file under desired name
        df.to_csv(directory+'data/'+dep_var_data[key],
                  columns=['date','val'],
                  index=False)

# TODO
# update datasets: will be useful when making website
def update_data(all_data=True,data_sets=[]):
    '''Updates data from online sources
    '''
    if all_data:
        val = 1
    else:
        val = 1
    return 0
