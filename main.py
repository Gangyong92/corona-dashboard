# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from data import (
    countries_df,
    totals_df,
    make_global_df,
    make_country_df,
    dropdown_options,
)
from builders import make_table


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",  # reset css
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",  # font style
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)
app.title = "Sexy Dashboard"
server = app.server

bubble_map = px.scatter_geo(
    countries_df,
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    hover_data={
        "Confirmed": ":,2f",
        "Recovered": ":,2f",
        "Deaths": ":,2f",
        "Country_Region": False,
    },
    size="Confirmed",
    size_max=40,
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    title="Confirmed By Country",
    projection="equirectangular",
)
bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)


bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={"count": ":,"},
    labels={
        "condition": "Condition",
        "count": "Count",
        "color": "Condition",
    },
)
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])


app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 50})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": "50",
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": "50",
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "color": "#111111",
                                "margin": "0 auto",
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country-graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("country-graph", "figure"),  # hello-output이라는 id를 가지는 곳에 children 쪽으로 출력함.
    [Input("country", "value")],  # hello-input이라는 id를 가지는 곳으로부터 value를 받음.
)
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()

    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={
            "value": ":,",
            "variable": False,
        },
        template="plotly_dark",
        color_discrete_map={
            "confirmed": "#e74c3c",
            "deaths": "#8e44ad",
            "recovered": "#27ae60",
        },
    )
    fig.update_xaxes(rangeslider_visible=True)

    return fig


