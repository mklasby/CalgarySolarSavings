import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

infos = ["As a rule of thumb we can install 1 kW of solar panels in 100 square feet of shadow free area on a reinforced cement concrete (RCC) roof.", "According to Energy Hub, solar panels in Alberta can produce about 1276 hours of energy.", "According to Energy Hub, installation cost of solar panels in Alberta is about $2.51 - $2.77/Watt."]

app.layout = html.Div([
    html.H3("Calculate the return on investment on a solar system"),
    html.Div([
            html.Ul(id='info-list', children=[html.Li(i) for i in infos])
    ]),
    html.Div(["Enter the size of the solar system: ",
              dcc.Input(id='panel_size', value=0, type='number'),
              html.Label(' kW')
              ]),
    html.Br(),
    html.Div(id='energy_gen')
])


@app.callback(
    Output(component_id='energy_gen', component_property='children'),
    Input(component_id='panel_size', component_property='value')
)
def output_energy_gen(input_value):
    if input_value != 0:
        return 'The average installation cost of a {:.0f} kW system in Alberta is between ${:.2f} and ${:.2f}. You can expect about {:.0f} kWh of energy production from this system. You can earn back you investment in {:.1f} to {:.1f} years assuming an average electricity cost of $0.167/kWh, without considering incentives.'.format(input_value, input_value*1000*2.51, input_value*1000*2.77, input_value*1276, input_value*1000*2.51/(1276*0.167*input_value), input_value*1000*2.77/(1276*0.167*input_value))

if __name__ == '__main__':
    app.run_server(debug=True)