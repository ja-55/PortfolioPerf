### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt

from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns


# Identify count of positive / negative performance months
pos = data_perf.loc[data_perf['Alpha'] > 0,'Alpha']
neg = data_perf.loc[data_perf['Alpha'] < 0,'Alpha']
pos = pos.groupby(pos.index.year).agg(['mean','count'])
neg = neg.groupby(neg.index.year).agg(['mean','count'])
neg = np.abs(neg)
pos['sign'] = 'positive'
neg['sign'] = 'negative'

# Organize positive / negative counts into dataframe
full = pd.concat([pos,neg]).reset_index().sort_values(by = ['Date','sign']).set_index(['Date','sign'])
counts = full.unstack().loc[:,('count','positive')]
m_alpha = full.unstack().loc[:,('mean','negative'):('mean','positive')]

# Close prior figure
plt.close()

# Histogram

fig_mrel, (ax_alphact,ax_alphamn, ax_alphahist) = plt.subplots(1,3, figsize = (15,5))

ax_alphahist.hist(data_perf.loc[:,'Alpha'], alpha = 0.7, bins = 10);
mu = data_perf.loc[:,'Alpha'].mean()
std = data_perf.loc[:,'Alpha'].std()
x = np.linspace(mu - 3 * std, mu + 3 * std, 100)
ax_alphahist.plot(x, norm.pdf(x, mu, std));

counts.plot.bar(ax = ax_alphact);
m_alpha.plot.line(ax = ax_alphamn, color = ['r','g']);

plt.suptitle('Monthly Alpha')
ax_alphact.title.set_text('Months Outperformed')
ax_alphamn.title.set_text('Average Alpha')
ax_alphahist.title.set_text('Alpha Distribution')

vals = ax_alphamn.get_yticks()
ax_alphamn.set_yticklabels(['{:,.0%}'.format(x) for x in vals]);
vals = ax_alphahist.get_xticks()
ax_alphahist.set_xticklabels(['{:,.0%}'.format(x) for x in vals]);
