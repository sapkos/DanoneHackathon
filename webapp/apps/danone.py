import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H2('Recipe parameters optimizer'),
    html.Div([
        dcc.Input(
            placeholder='fat_pct',
            type='number',
            value=''
            ),
        dcc.Input(
            placeholder='particles_grp1',
            type='number',
            value=''
            ),
        dcc.Input(
            placeholder='particles_grp2',
            type='number',
            value=''
            ),
        dcc.Input(
            placeholder='particles_grp3',
            type='number',
            value=''
            ),
        dcc.Input(
            placeholder='moisture',
            type='number',
            value=''
            )
        ]),
    html.Div([
        html.H3('Optimal parameters:'),
        ]),
    html.Div([
        html.Div([
            html.Div([
                html.P(
                    "wasser correction: ",
                    id = 'id1',
                    ),
                ]),
            html.Div([
                html.P(
                    "steam pressure: ",
                    id = 'id2',
                    ),
            ]),
            html.Div([
                html.P(
                    "sifthers speed: ",
                    id = 'id3',
                    ),
                ]),
            html.Div([
                html.P(
                    "speed dd: ",
                    id = 'id4',
                    ),
                ]),
            ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Tabs(id='expert-tabs', value='id1', children=[
                dcc.Tab(label='wasser correction', value='id1'),
                dcc.Tab(label='steam pressure', value='id2'),
                dcc.Tab(label='sifthers speed', value='id4'),
                dcc.Tab(label='speed dd', value='id5'),
                ]),
            html.Div(id='tabs-content')
            ], style={'width': '49%', 'display': 'inline-block'})
        ])
    ])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    return html.Div()
