### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt


### DATA SOURCES

path_mydata = 'Needs input'
path_rfr = 'Needs input'
tab_perf = 'Bal'
tab_sels = 'Inv'


### KEY PARAMETERS

roll_beta_wdw = 6
sell_wdw = 365
today = dt.date(2023,3,24)
sp500wts = {'Info Tech': 0.257, 'Health': 0.154, 'Comm': 0.108,
            'Fin': 0.106, 'C Disc': 0.105, 'Inds': 0.079,
            'C Stpl': 0.074, 'Util': 0.033, 'Energy': 0.03,
            'RE': 0.029, 'Mat': 0.025}
pfo_bal = 1234
pfo_crt_div = 1234


### READ IN AND CLEAN DATA

# Read in raw returns
data_perf_raw = pd.read_excel(path_mydata, sheet_name = tab_perf)
data_sels_raw = pd.read_excel(path_mydata, sheet_name = tab_sels)

# Work off of a copy
data_perf = data_perf_raw.copy()
data_sels = data_sels_raw.copy()

# Drop columns except portfolio and S&P returns
data_perf = data_perf.loc[:,['Date','P_R_%','SP_R_%']].dropna()
data_perf = data_perf.set_index('Date')

# Drop last row (incomplete period)
data_perf = data_perf.drop(data_perf.tail(1).index)

# Read in 3 month T-Bill as RFR
rfr = pd.read_csv(path_rfr)
rfr = rfr.rename(columns = {'DATE':'Date'})
rfr['Date'] = pd.to_datetime(rfr['Date'])
rfr = rfr.set_index('Date')
rfr = rfr.loc[data_perf.index[0]:data_perf.index[-1],:] / 100

# Convert 3 month T-bill to monthly rate
rfr = (1 + rfr) ** (1 / 12) - 1

# Adjust return series for T-bill rate
data_perf = data_perf.sub(rfr.values)

# Create Alpha column and set date
data_perf['Alpha'] = data_perf['P_R_%'] - data_perf['SP_R_%']

# Blank dataframes
df_op = pd.DataFrame(columns = ['Metric'])
df_compare = pd.DataFrame(index = data_perf.columns)
