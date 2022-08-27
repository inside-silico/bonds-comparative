import plotly.graph_objs as go 

def build_fig(trace):
    data = [trace]
    layout= dict(
        paper_bgcolor="#262626",

        template="plotly_dark",
        plot_bgcolor="#262626",

        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True
            ),
            type='date'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(rangeselector_bgcolor="black")

    return fig