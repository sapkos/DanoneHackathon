import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from sklearn.externals import joblib
import numpy as np
import json

from app import app

actual_values = {}

layout = html.Div([
    html.H2('Recipe parameters optimizer'),
    html.Div([
        dcc.Input(
            id='fat_pct',
            placeholder='fat_pct',
            type='number',
            value=None
            ),
        dcc.Input(
            id='part_1',
            placeholder='particles_grp1',
            type='number',
            value=None
            ),
        dcc.Input(
            id='part_2',
            placeholder='particles_grp2',
            type='number',
            value=None
            ),
        dcc.Input(
            id='part_3',
            placeholder='particles_grp3',
            type='number',
            value=None
            ),
        dcc.Input(
            id='moisture',
            placeholder='moisture',
            type='number',
            value=None
            ),
        html.Button('Calculate!', id='calculate-button')
        ]),
    html.Div([
        html.H3('Optimal parameters:'),
        ]),
    html.Div([
        html.Div([], id='parameters-div', style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Tabs(id='expert-tabs', value='water_correction', children=[
                dcc.Tab(label='wasser correction', value='water_correction'),
                dcc.Tab(label='steam pressure', value='steam_pressure'),
                dcc.Tab(label='sifthers speed', value='sifter_speed_nominal_pct'),
                dcc.Tab(label='speed dd', value='dd_speed'),
                ]),
            html.Div(id='tabs-content')
            ], style={'width': '49%', 'display': 'inline-block'})
        ])
    ])

@app.callback(Output('tabs-content', 'children'),
              [Input('expert-tabs', 'value')])
def render_content(tab):
    import ceterus_paribus as cp
    print(cp)
    import pandas as pd

    df = pd.read_csv('./data/recipe_0_out_reg.csv')
    model_efficiency = joblib.load('./models/recepta_0_model_efficiency.h5')
    with open('./models/recepta_0_cols_eff.json') as f:
        col_efficiency = json.load(f)
    values = actual_values.copy()
    fig_eff = cp.ceteris_paribus_plot(model_efficiency,
            values,
            tab,
            df,
            'efficiency',
            col_efficiency)

    model_bulk = joblib.load('./models/recepta_0_model_bulk_density.h5')
    with open('./models/recepta_0_cols_bulk_density.json') as f:
        col_bulk = json.load(f)
    fig_bulk = cp.ceteris_paribus_plot(model_bulk,
            values,
            tab,
            df,
            'bulk_density',
            col_bulk)

    df = pd.read_csv('./data/recipe_0_out_reg.csv')
    model_moisture = joblib.load('./models/recepta_0_model_moisture.h5')
    with open('./models/recepta_0_cols_moisture.json') as f:
        col_moisture = json.load(f)
    fig_moisture = cp.ceteris_paribus_plot(model_moisture,
            values,
            tab,
            df,
            'efficiency',
            col_moisture)
    print(fig_bulk.keys())

    return html.Div([
        dcc.Graph(
            figure=go.Figure(data=fig_eff['data'])
            ),
        dcc.Graph(
            figure=go.Figure(data=fig_bulk['data'])
            )
        ])

@app.callback(
        Output('parameters-div', 'children'),
        [Input('calculate-button', 'n_clicks')],
        [
            State('fat_pct', 'value'),
            State('part_1', 'value'),
            State('part_2', 'value'),
            State('part_3', 'value'),
            State('moisture', 'value')
        ])
def calculate_prediction(n_clicks, fat_pct, part_1, part_2, part_3, moisture):
    import find_optimal_values as fov
    import pandas as pd
    df = pd.read_csv('./data/recipe_0_out_reg.csv')
    model_efficiency = joblib.load('./models/recepta_0_model_efficiency.h5')
    with open('./models/recepta_0_cols_eff.json') as f:
        col_efficiency = json.load(f)
    vals_to_change = {k: np.NaN for k in col_efficiency}
    vals_to_change['fat_pct'] = fat_pct
    vals_to_change['particles_grp1'] = part_1
    vals_to_change['particles_grp2'] = part_2
    vals_to_change['particles_grp3'] = part_3
    vals_to_change['moisture'] = moisture


    new_vals, eff = fov.find_values_model_eff(
            model_efficiency,
            vals_to_change,
            df)
    actual_values.update(new_vals)
    return html.Div([
            html.Div([
                html.P(
                    f"water correction: {new_vals['water_correction']}",
                    id = 'id1',
                    ),
                ]),
            html.Div([
                html.P(
                    f"steam pressure: {new_vals['steam_pressure']}",
                    id = 'id2',
                    ),
            ]),
            html.Div([
                html.P(
                    f"sifthers speed: {new_vals['sifter_speed_nominal_pct']}",
                    id = 'id3',
                    ),
                ]),
            html.Div([
                html.P(
                    f"speed dd: {new_vals['dd_speed']}",
                    id = 'id4',
                    ),
                ]),
        ])
