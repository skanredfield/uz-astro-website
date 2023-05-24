import plotly.graph_objects as go

from datetime import datetime, timedelta

from django_plotly_dash import DjangoDash

from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from .models import WeatherData


external_stylesheets = [
    # 'main_app/style.css',
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP
]

app = DjangoDash('WeatherData_Text_DashApp', external_stylesheets=external_stylesheets)
app.css.append_css({ "external_url" : "/static/main_app/style.css" })
app.layout = html.Div([
    html.Div(id='live-update-text', style={'padding-bottom': '5px'}),
    dcc.Interval(
        id='interval-component',
        interval=1*60000, # in milliseconds
        n_intervals=0
    ),
])


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    # Last Reading: 2019-05-31 09:29:56 UTC
    # Temperature: 20.86 °C
    # Humidity: 15 %
    # Dew point: -6.73 °C
    # Wind speed: 32 km/h
    # Gust: 34 km/h
    # Brightness: Sunny
    # Rain: Dry
    # Clouds: Clear
    latest = WeatherData.objects.latest('reading_date', 'roof_safe_to_open', 'weather_permits_observations')
    is_safe = latest.roof_safe_to_open and latest.weather_permits_observations
    return [
        html.Div([
            html.Span('Safe to observe?', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span([
                dbc.Badge("Yes", color="success", className="me-1") if is_safe 
                else dbc.Badge("No", color="danger", className="me-1")
            ], style={'margin-left': '5px', 'fontSize': '16px'}),
        ]),
        html.Div([
            html.Span('Date and time: ', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span('{0}'.format(latest.get_formatted_datetime()), style={'margin-left': '5px', 'fontSize': '16px'}),
        ]),
        html.Div([
            html.Span('Temperature: ', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span('{0} °C'.format(latest.temperature), style={'margin-left': '5px', 'fontSize': '16px'}),
        ]),
        html.Div([
            html.Span('Wind: ', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span('{0} km/h'.format(latest.wind_level), style={'margin-left': '5px', 'fontSize': '16px'}),
        ]),
        html.Div([
            html.Span('Clouds temperature: ', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span('{0} °C'.format(latest.clouds_level), style={'margin-left': '5px', 'fontSize': '16px'}),
        ]),
        html.Div([
            html.Span('Humidity: ', style={'margin-left': '30px', 'fontSize': '16px'}),
            html.Span('{0}%'.format(latest.humidity_level), style={'margin-left': '5px', 'fontSize': '16px'}),
        ])
    ]

