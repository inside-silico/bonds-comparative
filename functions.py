from config import *
from numpy import diff
import plotly.graph_objs as go 
import numpy as np
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from sqlalchemy import create_engine
import pandas as pd
from layout import *
from layout_minimal import *
from pyhomebroker import HomeBroker
import datetime
from datetime import date





line1="#f4c100"
line2="#e6550d"
line3="#de2d26"

class graphics:
    def dual_tir(tir_ticker_selected,tir_ticker_selected2):
        engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}:{db_port}/{db}"
                    .format(user=db_usr,pw=db_pass,db_host=db_host,
                            db=db,db_port=db_port))

        df1=pd.read_sql_table(tir_ticker_selected,con=engine)
        df1.drop_duplicates(inplace=True)
        df1=df1[["date","TIR"]].copy()
        df1.TIR=df1.TIR*100
        df1.columns=["date","TIR1"]
        df2=pd.read_sql_table(tir_ticker_selected2,con=engine)
        df2.drop_duplicates(inplace=True)
        df2=df2[["date","TIR"]].copy()
        df2.TIR=df2.TIR*100
        df2.columns=["date","TIR2"]
        df=pd.DataFrame(columns=["date","TIR1","TIR2"])
        df.date=df1.date 
        df=df.set_index("date")
        df1=df1.set_index("date")
        df.update(df1)
        df2=df2.set_index("date")
        df.update(df2)
        df=df.reset_index()
        df = df[df['TIR1'] > 0] 
        df = df[df['TIR2'] > 0] 
        df=df.replace(0,np.nan)
        df=df.dropna()

        fig = go.Figure(layout=go.Layout(layout.layout_minimal()))

        fig.add_trace(go.Scatter(x=df.date, y=df.TIR1,name=tir_ticker_selected,line=dict(color=line1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.TIR2,name=tir_ticker_selected2,line=dict(color=line2)))
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(title='TIR', title_x=0.5)
        #fig.update_traces(line=dict(width=2,color='yellow'))
        fig.update_xaxes(rangeselector_bgcolor="black")
        page = fig
        return page

    def diff_par(tir_ticker_selected,tir_ticker_selected2):
        engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}:{db_port}/{db}"
                    .format(user=db_usr,pw=db_pass,db_host=db_host,
                            db=db,db_port=db_port))
        df1=pd.read_sql_table(tir_ticker_selected,con=engine)
        df1.drop_duplicates(inplace=True)
        df1=df1[["date","PAR"]].copy()
        df1.columns=["date","Paridad1"]
        

        df2=pd.read_sql_table(tir_ticker_selected2,con=engine)
        df2.drop_duplicates(inplace=True)
        df2=df2[["date","PAR"]].copy()
        df2.columns=["date","Paridad2"]

        df=pd.DataFrame(columns=["date","Paridad1","Paridad2","DiffPar"])
        df.date=df1.date 
        df=df.set_index("date")
        df1=df1.set_index("date")
        df.update(df1)
        df2=df2.set_index("date")
        df.update(df2)
        df.DiffPar=(df.Paridad1-df.Paridad2)*100
        df=df.reset_index()
        df=df.replace(0,np.nan)
        df=df.dropna()

        trace = go.Scatter(x=list(df.date), y=list(df.DiffPar))

        fig=build_fig(trace)
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(title='Diferencia de paridades '+tir_ticker_selected+'/'+tir_ticker_selected2, title_x=0.5)
        fig.update_traces(line=dict(width=2,color='yellow'))


        return fig

    def dual_par(tir_ticker_selected,tir_ticker_selected2):
        engine = create_engine("mysql+pymysql://{user}:{pw}@{db_host}:{db_port}/{db}"
                    .format(user=db_usr,pw=db_pass,db_host=db_host,
                            db=db,db_port=db_port))

        df1=pd.read_sql_table(tir_ticker_selected,con=engine)
        df1.drop_duplicates(inplace=True)
        df1=df1[["date","PAR"]].copy()
        df1.columns=["date","TIR1"]
        df2=pd.read_sql_table(tir_ticker_selected2,con=engine)
        df2.drop_duplicates(inplace=True)

        df2=df2[["date","PAR"]].copy()
        df2.columns=["date","TIR2"]
        df=pd.DataFrame(columns=["date","TIR1","TIR2"])
        df.date=df1.date 
        df=df.set_index("date")
        df1=df1.set_index("date")
        df.update(df1)
        df2=df2.set_index("date")
        df.update(df2)
        df=df.reset_index()
        df=df.replace(0,np.nan)
        df=df.dropna()        
        fig = go.Figure(layout=go.Layout(layout.layout_minimal()))

        fig.add_trace(go.Scatter(x=df.date, y=df.TIR1,name=tir_ticker_selected,line=dict(color=line1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.TIR2,name=tir_ticker_selected2,line=dict(color=line2)))
        #fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(title='Paridad', title_x=0.5)
        #fig.update_traces(line=dict(width=2,color='yellow'))
        fig.update_xaxes(rangeselector_bgcolor="black")
        page = fig
        return page

    def ratio(tir_ticker_selected,tir_ticker_selected2):

        df1=hb.history.get_daily_history(tir_ticker_selected, datetime.date(2005,1, 1), today)
        df1.drop_duplicates(inplace=True)
        df1=df1[["date","close"]].copy()
        df1.columns=["date","Paridad1"]
        

        df2=hb.history.get_daily_history(tir_ticker_selected2, datetime.date(2005,1, 1), today)
        df2.drop_duplicates(inplace=True)
        df2=df2[["date","close"]].copy()
        df2.columns=["date","Paridad2"]

        df=pd.DataFrame(columns=["date","Paridad1","Paridad2","DiffPar"])
        df.date=df1.date 
        df=df.set_index("date")
        df1=df1.set_index("date")
        df.update(df1)
        df2=df2.set_index("date")
        df.update(df2)
        df.DiffPar=(df.Paridad1/df.Paridad2)*100
        df=df.reset_index()
        df=df.replace(0,np.nan)
        df=df.dropna()

        trace = go.Scatter(x=list(df.date), y=list(df.DiffPar))

        fig=build_fig(trace)
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(title='Ratio '+tir_ticker_selected+'/'+tir_ticker_selected2, title_x=0.5)
        fig.update_traces(line=dict(width=2,color=line1))


        return fig
