import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams
import statsmodels.api as sm
import itertools
import plotly.express as px

filename = "../data/Energy_Consumer_Prices_Index.csv"
missing_values = ["n/a", "na", "--", "NaN"]
energy_prices = pd.read_csv(filename, na_values = missing_values)
energy_prices['Year'] =  pd.to_datetime(energy_prices.Year, format='%Y')
energy_prices = energy_prices.set_index('Year')
y_energy = energy_prices['CPI'].resample('Y').sum()

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y_energy,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

mod = sm.tsa.statespace.SARIMAX(y_energy,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
# print(results.summary().tables[1])

pred_uc = results.get_forecast(steps=25)
pred_ci = pred_uc.conf_int(alpha=0.80)

# Regular plot via matplotlib
# ax = y_energy.plot(label='observed', figsize=(14, 7))
# pred_uc.predicted_mean.plot(ax=ax, label='Forecast')

# ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.1)

# ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2021-12-31'), y_energy.index[-1], alpha=.01, zorder=-2)

# ax.set_xlabel('Year')
# ax.set_ylabel('Energy Consumer Price Index $ USD')
# ax.set_title('Energy Consumer Price Index Forecast')
# plt.legend()
# plt.show()


# Plotly version

fig = px.line(x=y_energy.index, y=y_energy.values, title="Energy Consumer Price Index", labels=dict(x="Year", y="Consumer Price Index for Energy", color="Place"))
fig.add_scatter(x=pred_ci.index, y=pred_ci['lower CPI'])
fig.update_layout(showlegend=False)
fig.show()


