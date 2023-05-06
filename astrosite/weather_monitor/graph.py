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

app = DjangoDash('WeatherData_DashApp', external_stylesheets=external_stylesheets)
app.css.append_css({ "external_url" : "/static/main_app/style.css" })
app.layout = html.Div([
    html.Div(id='live-update-text', style={'padding-bottom': '5px'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-dataset',
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
            style={'width': '50%', 'margin-left': '30px', 'margin-right': '5px'}
        ),
        html.Div([
            dcc.Dropdown(
                id='dropdown-range',
                options=[
                    {'label': 'Last 24 hours', 'value': 'last_24_hours'},
                    {'label': 'Last 3 days', 'value': 'last_3_days'},
                    {'label': 'Last week', 'value': 'last_week'},
                    {'label': 'Last month','value': 'last_month'},
                    {'label': 'Last year','value': 'last_year'},
                ],
                value='last_24_hours',
                clearable=False
                
            )],
            style={'width': '50%', 'margin-left': '5px', 'margin-right': '10px'}
        )],
        style={'display': 'flex'}
    ),
    html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*60000, # in milliseconds
            n_intervals=0
        ),
    ])
])


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    latest = WeatherData.objects.latest('reading_date', 'roof_safe_to_open', 'weather_permits_observations')
    is_safe = latest.roof_safe_to_open and latest.weather_permits_observations
    return [
        html.Span('Safe to observe?', style={'margin-left': '30px', 'fontSize': '16px'}),
        html.Span([
            dbc.Badge("Yes", color="success", className="me-1") if is_safe 
            else dbc.Badge("No", color="danger", className="me-1")
        ], style={'margin-left': '5px', 'fontSize': '16px'}),
        html.Span('(@ {0})'.format(latest.reading_date), style={'margin-left': '5px', 'fontSize': '16px'}),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'),
              Input('dropdown-dataset', 'value'),
              Input('dropdown-range', 'value'))
def update_graph_live(n, value_dataset, value_range):
    if value_range == "last_24_hours":
        time_range = datetime.now() - timedelta(days=1)
        weather_data = WeatherData.objects.filter(reading_date__gte=time_range).order_by("-reading_date")
    elif value_range == "last_3_days":
        time_range = datetime.now() - timedelta(days=3)
        weather_data = WeatherData.objects.filter(reading_date__gte=time_range).order_by("-reading_date")
    elif value_range == "last_week":
        time_range = datetime.now() - timedelta(days=7)
        weather_data = WeatherData.objects.filter(reading_date__gte=time_range).order_by("-reading_date")
    elif value_range == "last_month":
        time_range = datetime.now() - timedelta(days=30)
        weather_data = WeatherData.objects.filter(reading_date__gte=time_range).order_by("-reading_date")
    elif value_range == "last_year":
        time_range = datetime.now() - timedelta(days=365)
        weather_data = WeatherData.objects.filter(reading_date__gte=time_range).order_by("-reading_date")
    else:
        weather_data = WeatherData.objects.order_by("-reading_date")[:250]


    if value_dataset == "clouds":
        return draw_figure("clouds", weather_data, "clouds_level")
    elif value_dataset == "temperature":
        return draw_figure("temperature", weather_data, "temperature")
    elif value_dataset == "wind":
        return draw_figure("wind", weather_data, "wind_level")
    elif value_dataset == "gust":
        return draw_figure("gust", weather_data, "wind_gust_level")
    elif value_dataset == "rain":
        return draw_figure("rain", weather_data, "rain_level")
    elif value_dataset == "light":
        return draw_figure("light", weather_data, "light_level")
    elif value_dataset == "humidity":
        return draw_figure("humidity", weather_data, "humidity_level")
    elif value_dataset == "dew":
        return draw_figure("dew", weather_data, "dew_point")

def draw_figure(data_field_name: str, weather_data, attr_name: str):
    data = {
        'time': [],
        data_field_name: []
    }

    for entry in weather_data:
        data['time'].append(entry.reading_date)
        data[data_field_name].append(getattr(entry, attr_name))

    fig = go.Figure()
    fig.update_layout(template="plotly_white")
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.add_trace(go.Scatter(x=data['time'], y=data[data_field_name],
                    mode='lines+markers',
                    name=data_field_name))

    return fig
