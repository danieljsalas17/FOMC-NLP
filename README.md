# FOMC-NLP

My goal for this project is to use NLP techniques for an in-depth analysis into the patterns and effects of the Federal Reserve's language. First, I will practice unsupervised learning models on a small sample of FOMC official statements. Then, I will try a few supervised learning models with a few different target variables. Once I'm done practicing on the small sample, I'd like to set up a data pipeline and long running project that continually updates analyses of the language of all Federal Reserve Press Releases.

## Unsupervised Learning Methods

Cluster analysis, PCA, SVD, and possibly autoencoding NNs. Examples in the jupyter notebook `Preliminary Text Analysis.ipynb`

## Supervised Learning Methods

#### Targets
Before considering which supervised learning methods, I need to consider which target variables are of interest. A few here that are worth trying:
* fed funds rate
* T-bill rates: 3m up to 10y
* Slope of yield curve (constructed from T-bill data)
* S&P 500 and other equity indices

#### Methods
Gradient boosted regressors (XGboost), random forest, Naive Bayes, regularized regression (Lasso), NN models

## Expanding the Data

I am concerned with the timing of the press releases, so the data have time series structure. The tricky thing will be how to deal with press releases on the same day. I could order them by time of day as well, but even then, there may be overlap. I could append simultaneous press releases into one observation, but that may get messy. For now, I am just hoping that if I sort only by Monetary Policy press releases, I won't run into that issue.

The first `fed_sample_statements.json` dataset will only contain FOMC statements going back to 2012 (got lazy, so doesn't have every statement, but .

## Goals

Get working text analysis models on the sample, and then move onto web scrapers to gather data other than just the FOMC statements going back to 2014. This could include the implementation notes, releases of minutes, regulation announcements, notes on strategy, etc. Eventually, I'm going to have to figure out how to use some pdf readers (not all of these are html).
