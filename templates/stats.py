import dash
import calendar
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def get_figs():
    filename = "data/Corporate_Energy_Consumption.csv"
    df = pd.read_csv(filename)
    df['Total Consumption'][df['Unit'] == 'GJ'] *= 277.778
    df['Unit'].replace('GJ', 'kWh')

    # pie chart of energy breakdown by type
    energy_breakdown = df.groupby(['Energy Description'])[
        'Total Consumption'].sum().reset_index()
    fig = px.pie(energy_breakdown, values='Total Consumption', names='Energy Description',
                 title="Business Units' Energy Utilization (in kW) Breakdown in Calgary")

    # line graphs of energy usage by year and type
    energy_by_year = df.groupby(
        ['Year'])['Total Consumption'].sum().reset_index()
    energy_bd_year = df.groupby(['Energy Description', 'Year'])[
        'Total Consumption'].sum().reset_index()

    fig2 = px.line(energy_by_year, x='Year', y='Total Consumption',
                   title="Business Units' Total Yearly Energy Utilization (in kW) in Calgary")
    fig3 = px.line(energy_bd_year, x='Year', y='Total Consumption', color='Energy Description',
                   title="Business Units' Energy Utilization Breakdown (in kW) in Calgary")

    # line graph of energy usage by month
    monthly_energy = df.groupby(['Month', 'Year']).agg(
        {'Total Consumption': 'sum'}).reset_index()

    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    calendar_month = calendar.month_name[1:]
    month = {month[i]: calendar_month[i] for i in range(len(month))}
    monthly_energy['Month'] = monthly_energy['Month'].replace(month)
    monthly_energy['Month'] = pd.Categorical(
        monthly_energy.Month, categories=calendar_month, ordered=True)
    monthly_energy = monthly_energy.sort_values('Month')
    fig4 = px.line(monthly_energy, x='Month', y='Total Consumption', color='Year',
                   title="Business Units' Monthly Energy Utilization (in kW) in Calgary")

    app = dash.Dash(prevent_initial_callbacks=True)
    app.layout = html.Div([
        dcc.Location(id="url"),
        html.Div(
            [dcc.Graph(id="graph1", figure=fig, style={'width': '80vw'})]),
        html.Div([dcc.Graph(id="graph2", figure=fig2, style={
                  'width': '80vw', 'height': '80vh'})]),
        html.Div([dcc.Graph(id="graph3", figure=fig3, style={
                  'width': '80vw', 'height': '80vh'})]),
        html.Div([dcc.Graph(id="graph4", figure=fig4, style={
                 'width': '80vw', 'height': '80vh'})])
    ])
    return fig.to_html(), fig2.to_html(), fig3.to_html(), fig4.to_html()
