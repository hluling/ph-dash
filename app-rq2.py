#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script creates the RQ2 dashboard in the Programming Historian Lesson - "Creating a Dashboard for Interactive Data Visualization with Dash in Python."
"""

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Define a function to conditionally format the text
# Don't show percentages on pie chart under 4%
def format_text(pct):
    return f'{pct:.1f}%' if pct >= 4 else ''

lang_asrow = pd.read_csv("data/data_lang_asrow.csv", encoding="utf-8", index_col=[0])
lang_asrow_noeng = lang_asrow.drop(['English'])
lang_asrow_noeng.columns = lang_asrow_noeng.columns.astype(str)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

app.layout = dbc.Container(
         [   
        dbc.Row([ # row 1
            dbc.Col([html.H1('Top 10 Non-English Newspaper Languages in the U.S.')],
                    className="text-center mt-3 mb-1")
        ]
    ),
        dbc.Row([ # row 2
            dbc.Col( # left column
                dbc.Row([
                dbc.Label("Select a decade:", className="fw-bold"),
                dcc.Dropdown(id='years_left',
                        options=lang_asrow_noeng.columns,
                        value='1690', clearable=False
                        ),
            dcc.Graph(id="graph_left")
            ]),
                width=6
            ),
            dbc.Col( # right column
                dbc.Row([
                dbc.Label("Select a decade:", className="fw-bold"),
                dcc.Dropdown(id='years_right',
                        options=lang_asrow_noeng.columns,
                        value='2020', clearable=False
                ),
            dcc.Graph(id="graph_right")
            ]),
                width=6,
            ),
        ])
], fluid=True)

@app.callback(
    Output("graph_left", "figure"),
    Output("graph_right", "figure"),
    Input("years_left", "value"),
    Input("years_right", "value")
    )
def generate_chart(year_left, year_right):
    df_left = lang_asrow_noeng[year_left].sort_values(ascending = False).reset_index().head(10)

    df_left.loc[len(df_left)] = ["Others", lang_asrow_noeng[year_left].sort_values(ascending = False).reset_index().iloc[10:][year_left].sum()]

    df_left = df_left.rename(columns={"index": "Language", year_left: "Count"})

    #df_left.head()
    fig_left = px.pie(df_left, values="Count", names="Language", hole=.6,
                color_discrete_sequence=px.colors.sequential.RdBu,
                )
    
    fig_left.update_layout(
        width=700,  
        height=700,
        legend=dict(font=dict(size=20),
                    x=1.4,  
                    y=0.5,  
                    xanchor='left',  
                    yanchor='middle'))
    
    fig_left.update_traces(
    textinfo='percent',
    texttemplate=[format_text(pct) for pct in df_left['Count'] / df_left['Count'].sum() * 100],
    hovertemplate='%{label}<br>%{percent:.1%}<extra></extra>',
    textfont=dict(size=20)
    )
    
    df_right = lang_asrow_noeng[year_right].sort_values(ascending = False).reset_index().head(10)
    
    df_right.loc[len(df_right)] = ["Others", lang_asrow_noeng[year_right].sort_values(ascending = False).reset_index().iloc[10:][year_right].sum()]

    df_right = df_right.rename(columns={"index": "Language", year_right: "Count"})
    
    fig_right = px.pie(df_right, values="Count", names="Language", hole=.6,
                color_discrete_sequence=px.colors.sequential.RdBu)
    
    fig_right.update_layout(
        width=700,  
        height=700,
        legend=dict(font=dict(size=20),
                    x=1.4,  
                    y=0.5,  
                    xanchor='left',
                    yanchor='middle'))
    
    fig_right.update_traces(
    textinfo='percent',
    texttemplate=[format_text(pct) for pct in df_right['Count'] / df_right['Count'].sum() * 100],
    textfont=dict(size=20),
    hovertemplate='%{label}<br>%{percent:.1%}<extra></extra>',
    )

    return fig_left, fig_right

if __name__ == '__main__':
    app.run(debug=True)