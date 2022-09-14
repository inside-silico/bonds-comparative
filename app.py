import os
import plotly.graph_objs as go 
import dash
import mysql.connector
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from layout import *
from layout_minimal import *

from functions import *

app = dash.Dash(__name__,suppress_callback_exceptions=True)

server = app.server

db_host="comparative-db"
db_pass="db_user_pass"
db_usr="db_user"

def single_tir(ticker):

    engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}/{db}"
                       .format(user=db_usr,pw=db_pass,db_host=db_host,
                               db="bonds_tir",))

    df=pd.read_sql_table(ticker,con=engine)
    df.TIR=df.TIR*100

    trace = go.Scatter(x=list(df.date), y=list(df.TIR))

    fig=build_fig(trace)
    fig.update_yaxes(fixedrange=False)
    fig.update_layout(title=ticker+' TIR', title_x=0.5)
    fig.update_traces(line=dict(width=2,color='yellow'))
    
    page =html.Div(children=[
        dcc.Graph(
        figure=fig)])
    return page



def diff_page():
    mydb = mysql.connector.connect(
        host="comparative-db",
        user="db_user",
        password="db_user_pass",
        db="bonds_tir"
    )

    
    mycursor = mydb.cursor()
    mycursor.execute("Show tables;")
    myresult = list(mycursor)
    out = [item for t in myresult for item in t]

    available_indicators = out
    page = html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='tir_ticker_selected',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='AL30D'
                    ),
                ], style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='tir_ticker_selected2',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='GD30D'
                    ),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Div([
                dcc.Graph(id='dual_par_graph'),

            ],style={"padding-top":"50px"}),

            html.Div([
                dcc.Graph(id='dual_tir_graph'),

            ],style={"padding-top":"50px"}),

            html.Div([
                dcc.Graph(id='diff_par_graph'),

            ],style={"padding-top":"50px"}),            
        ])
    return page


index_layout = html.Div( [ html.H3('Escribi bien salame')   ])
app.layout = html.Div(dcc.Location(id="url", refresh=True),id="page-content")


@app.callback(
    dash.dependencies.Output('diff_par_graph', 'figure'),
    [dash.dependencies.Input('tir_ticker_selected', 'value'),
    dash.dependencies.Input('tir_ticker_selected2', 'value')])
def update_graph(tir_ticker_selected,tir_ticker_selected2):
    return graphics.diff_par(tir_ticker_selected,tir_ticker_selected2)


@app.callback(
    dash.dependencies.Output('dual_tir_graph', 'figure'),
    [dash.dependencies.Input('tir_ticker_selected', 'value'),
    dash.dependencies.Input('tir_ticker_selected2', 'value')])
def update_graph2(tir_ticker_selected,tir_ticker_selected2):
    return graphics.dual_tir(tir_ticker_selected,tir_ticker_selected2)

@app.callback(
    dash.dependencies.Output('dual_par_graph', 'figure'),
    [dash.dependencies.Input('tir_ticker_selected', 'value'),
    dash.dependencies.Input('tir_ticker_selected2', 'value')])
def update_graph3(tir_ticker_selected,tir_ticker_selected2):
    return graphics.dual_par(tir_ticker_selected,tir_ticker_selected2)

@app.callback(
    dash.dependencies.Output('ratio_graph', 'figure'),
    [dash.dependencies.Input('tir_ticker_selected', 'value'),
    dash.dependencies.Input('tir_ticker_selected2', 'value')])
def update_graph4(tir_ticker_selected,tir_ticker_selected2):
    return graphics.ratio(tir_ticker_selected,tir_ticker_selected2)



@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname="/"):
    ctx = dash.callback_context
    triggered_by = ctx.triggered[0].get("prop_id")

    if pathname ==  "/dif-par":
        page=diff_page()
        return page
    
    else:
        return index_layout

if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0')
