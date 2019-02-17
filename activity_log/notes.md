## Feb 14 2019

Created repository and started working. Things accomplished:
* Made sample datasets
* Started NLP example notebook
	* Got as far as PCA scree plots

### TODO
* Get dependent variable data
	* interest rate data
	* chairman at time
* Clean up some of the notebook scripts and package them into a .py file for later use
* Try other unsupervised learning models, i.e. clusters
* Try supervised learning models (once a dependent var is chosen)

### TODO: at later date
* Begin setting up scraping algo
	* First, just all FOMC meeting statements
	* Next, include all press releases (after figuring out pdfreaders)
* Flask app
* AWS
	* EC2 for Flask app and collecting Federal Reserve statements
	* S3 for Storage of statements
* Update app for PySpark  

## Feb 17 2019

### Goals for today
* Write function that takes a datetime and returns who is the fed chairman. This will be useful for a language classification problem.
* Obtain interest rate data: 3m and 10y Tbill rates, Fed Funds, and possibly some equity indices (may not actually be that useful, since I'm not sure how often markets in aggregate actually move in response to FOMC statements or Fed Press Releases)
	* Make sure to give data file these names: `T-bill_3m.csv`, `T-bill_10y.csv`, `fedfunds.csv`, `sp500_dailyclose.csv`
* Clean up some scripts in the Preliminary Text Analysis notebook and start a mini module of useful functions.
* Once module and dependent variables are done, start trying some supervised learning models (NNs if you have time).
