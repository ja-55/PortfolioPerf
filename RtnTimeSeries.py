### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt

from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# Set up chart space
fig_tsperf, (ax_ts_perf_ln, ax_ts_perf_br) = plt.subplots(2,1, figsize = (15,10))
ax_ts_perf_ln.title.set_text('Cumulative Returns')
ax_ts_perf_br.title.set_text('Annual Returns')
plt.suptitle('Time Series Performance', fontweight = 'bold')

# Cumulative Performance
cum_mr = (1 +data_perf.drop('Alpha', axis = 1)).cumprod() - 1
cum_mr.plot.line(ax = ax_ts_perf_ln);

# Annual Performance
df_compare_ann = data_perf.groupby(data_perf.index.year).apply(lambda x: (1 + x).prod() - 1).drop('Alpha', axis = 1)
df_compare_ann.plot.bar(ax = ax_ts_perf_br);

# Labeling
vals = ax_ts_perf_br.get_yticks()
ax_ts_perf_br.set_yticklabels(['{:,.0%}'.format(x) for x in vals]);
vals = ax_ts_perf_ln.get_yticks()
ax_ts_perf_ln.set_yticklabels(['{:,.0%}'.format(x) for x in vals]);
