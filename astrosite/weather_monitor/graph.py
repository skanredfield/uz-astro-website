import plotly
from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output

from .models import WeatherData


external_stylesheets = [
    'weather_monitor/style.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = DjangoDash('WeatherData_DashApp', external_stylesheets=external_stylesheets)
app.layout = html.Div([
    # html.Div([
    #     html.H4('Weather Data'),
    # ]),
    html.Div([
        dcc.Dropdown(
            id='dropdown1',
            options=[
                {'label': 'Clouds', 'value': 'clouds'},
                {'label': 'Temperature', 'value': 'temperature'},
                {'label': 'Wind', 'value': 'wind'},
                {'label': 'Wind Gust','value': 'gust'},
                {'label': 'Rain','value': 'rain'},
                {'label': 'Light','value': 'light'},
                {'label': 'Humidity','value': 'humidity'},
                {'label': 'Dew Point','value': 'dew'},
            ],
            value='wind',
            clearable=False
            
        )],
        style={'width': '20%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*60000, # in milliseconds
            n_intervals=0
        )
    ])
])


# @app.callback(Output('live-update-text', 'children'),
#               Input('interval-component', 'n_intervals'))
# def update_metrics(n):
#     # lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#     wind = get_wind_reading(get_weather_data())

#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         # html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#         # html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#         # html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#         html.Span('Current wind: {0:0.2f}'.format(wind), style=style)
#     ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'),
              Input('dropdown1', 'value'))
def update_graph_live(n, drop_value):
    weather_data = WeatherData.objects.order_by("-reading_date")[:250]

    if drop_value == "clouds":
        return draw_figure("clouds", weather_data, "clouds_level")
    elif drop_value == "temperature":
        return draw_figure("temperature", weather_data, "temperature")
    elif drop_value == "wind":
        return draw_figure("wind", weather_data, "wind_level")
    elif drop_value == "gust":
        return draw_figure("gust", weather_data, "wind_gust_level")
    elif drop_value == "rain":
        return draw_figure("rain", weather_data, "rain_level")
    elif drop_value == "light":
        return draw_figure("light", weather_data, "light_level")
    elif drop_value == "humidity":
        return draw_figure("humidity", weather_data, "humidity_level")
    elif drop_value == "dew":
        return draw_figure("dew", weather_data, "dew_point")

def draw_figure(data_field_name: str, weather_data, attr_name: str):
    data = {
        'time': [],
        data_field_name: []
    }

    for entry in weather_data:
        data['time'].append(entry.reading_date)
        data[data_field_name].append(getattr(entry, attr_name))

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data[data_field_name],
        'name': data_field_name,
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig
