import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams
import statsmodels.api as sm
import itertools
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

def get_figs():
  filename = "../data/Carbon_Tax_Per_Jurisdiction.csv"

  missing_values = ["n/a", "na", "--", "NaN"]
  data = pd.read_csv(filename, na_values = missing_values)
  column_names = data.columns

  # Pre-processing
  for i in column_names:
    if ('Price_label' in i) or ('Instrument' in i) or ('Price_rate_2' in i):
      data.drop(i , axis='columns', inplace=True)

  # drop Name of Initiative
  data.drop('Name of the initiative', axis='columns', inplace=True)

  # rename time related column names accordingly, keep only time related substring
  column_names = data.columns
  for i in column_names:
    if ('Price_rate_1_' in i):
      new_col_name = i.replace('Price_rate_1_','')
      data.rename(columns = {i:new_col_name}, inplace = True)
    if ('Price_rate_2_' in i):
      new_col_name = i.replace('Price_rate_2_','')
      data.rename(columns = {i:new_col_name}, inplace = True)

  # data.reset_index(drop=True, inplace=True)
  index_names = data[ data['Jurisdiction Covered'] != 'Alberta' ].index 
  data.drop(index_names, inplace = True)

  data.drop(1, inplace = True)
  data.drop('Jurisdiction Covered', axis='columns', inplace = True)

  # Convert into time series like shape
  timeSeries = data.transpose()
  timeSeries.rename(columns = {0:'carbon_price'}, inplace = True) 
  timeSeries.reset_index( inplace=True)
  timeSeries.rename(columns = {'index':'year'}, inplace = True) 

  # Change type to date time to be able to resample
  timeSeries.year = timeSeries.year.astype(str).astype(float)
  timeSeries['year'] =  pd.to_datetime(timeSeries.year, format='%Y')
  timeSeries = timeSeries.set_index('year')
  y = timeSeries['carbon_price'].resample('Y').sum()

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
              mod = sm.tsa.statespace.SARIMAX(y,
                                              order=param,
                                              seasonal_order=param_seasonal,
                                              enforce_stationarity=False,
                                              enforce_invertibility=False)
              results = mod.fit()
              # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
          except:
              continue

  mod = sm.tsa.statespace.SARIMAX(y,
                                  order=(1, 1, 1),
                                  seasonal_order=(1, 1, 0, 12),
                                  enforce_stationarity=False,
                                  enforce_invertibility=False)
  results = mod.fit()
  # print(results.summary().tables[1])

  pred_uc = results.get_forecast(steps=15)
  pred_ci = pred_uc.conf_int(alpha=0.95)

  ### Regular plot on matplotlib
  # ax = y.plot(label='observed', figsize=(14, 7))

  # pred_uc.predicted_mean.plot(ax=ax, label='Forecast')

  # ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.1)

  # ax.set_xlabel('Date')
  # ax.set_ylabel('Carbon Tax in Alberta')

  # plt.legend()
  # plt.show()

  ### Plotly version
  # Prediction of Energy Prices / Energy Consumer Price Index
  fig = px.line(x=y.index, y=y.values, title="Carbon Tax Prediction in Alberta", labels=dict(x="Year", y="Tax $", color="Place"))
  fig.add_scatter(x=pred_ci.index, y=pred_ci['lower carbon_price'])
  fig.update_layout(showlegend=False)
  # fig.show()

  # Rendering on the page
  app = dash.Dash(prevent_initial_callbacks=True)
  app.layout = html.Div([dcc.Location(id="url"), html.Div([dcc.Graph(id="graphCarbonTax", figure=fig, style={'width': '80vw'})])])
  return fig.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
