import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
        'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s8.css',
        'https://github.com/plotly/dash-salesforce-crm/blob/master/static/s4.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
