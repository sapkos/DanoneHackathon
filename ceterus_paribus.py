def ceteris_paribus_plot(model, values, col, df, trace_name):
    """
    Function to plot ceterus paribus values of model
    """
    distinct_values = sorted(df[col].unique())
    preds_single = model.predict(pd.DataFrame(values, index=[0])[cols])[0]
    first_value = values[col]
    preds = []
    for value in distinct_values:
        values[col] = value
        preds.append(model.predict(pd.DataFrame(values, index=[0])[cols])[0])
    trace = go.Scatter(
    x = distinct_values,
    y = preds,
        name=trace_name
    )
    trace2 = go.Scatter(x=[first_value], y=[preds_single],
                   marker = dict(
            size = 10,
            color = 'rgba(152, 0, 0, .8)',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )),
                       name="Actual value")
    data = [trace, trace2]

    layout = dict(title = f'Ceterus paribus plot for {col}',
                  )

    fig = dict(data=data, layout=layout)
    return fig
