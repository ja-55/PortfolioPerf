### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt

from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns


# Calculate Rolling Beta
numer = data_perf.loc[:,'P_R_%'].rolling(window = roll_beta_wdw).cov(data_perf.loc[:,'SP_R_%']).dropna()
denom = data_perf.loc[:,'SP_R_%'].rolling(window = roll_beta_wdw).var().dropna()
roll_beta = numer / denom
roll_beta.name = 'Rolling Beta'


# Close prior figure
plt.close()


# Plot Rolling Beta
fig_rbeta, ax_rbeta = plt.subplots(1,1, figsize = (15,5))
roll_beta.plot.line(ax = ax_rbeta)

# Plot fitted trendline
srs = np.array(range(roll_beta.shape[0]))
z = np.polyfit(srs, roll_beta.values, 1)
p = np.poly1d(z)

tline = pd.DataFrame([roll_beta.index,p(srs)]).T
tline = tline.rename(columns = {0:'Date',1:'Trend'})
tline = tline.set_index('Date')


tline.plot.line(ax = ax_rbeta, color = 'r', linestyle = '--')
plt.axhline(y = 1, color = 'black', linestyle = ':', label = 'Beta = 1')
plt.axhline(y = roll_beta.mean(), color = 'green', linestyle = ':', label = 'Mean Beta')
plt.suptitle('Rolling Beta: Window = {} Months'.format(roll_beta_wdw))
plt.legend()
plt.annotate('Mean Beta = %.2f'%(roll_beta.mean()), xy = (10,120), xycoords = 'axes points');
#plt.annotate(\"Beta = 1.0\", xy = (10,235), xycoords = 'axes points');
#plt.annotate(\"Trendline Equation: y=%.4fx+%.4f\"%(z[0],z[1]), xy = (600,100), xycoords = 'axes points');
