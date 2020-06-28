from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from joblib import load
import numpy as np
import pandas as pd

import titanic_functions as tfunc

from app import app


style = {'padding': '1.5em'}


layout = html.Div([
    dcc.Markdown("""
        ### Predict
        Input your details to see if you would have survived the Titanic disaster.
    """),
    html.Div(id='prediction-content', style={'fontWeight': 'bold'}),
    html.Div([
        dcc.Markdown('###### Ticket Class'),
        dcc.Input(id="pclass"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Name'),
        dcc.Input(id="name"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Sex'),
        dcc.Input(id="sex"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Age'),
        dcc.Input(id="age"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Siblings-Spouse'),
        dcc.Input(id="sibsp"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Parents-Children'),
        dcc.Input(id="parch"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Fare'),
        dcc.Input(id="fare"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Cabin'),
        dcc.Input(id="cabin"),
    ], style=style),

    html.Div([
        dcc.Markdown('###### Embarked'),
        dcc.Input(id="embarked"),
    ], style=style) 
    ], style = {'columnCount': 1})

@app.callback(Output('prediction-content', 'children'),
             [Input('pclass', 'value'),
             Input('name', 'value'),
             Input('sex', 'value'),
             Input('age', 'value'),
             Input('sibsp', 'value'),
             Input('parch', 'value'),
             Input('fare', 'value'),
             Input('cabin', 'value'),
             Input('embarked', 'value')])

def predict(pclass, name, sex, age, sibsp, parch, fare, cabin, embarked):

    # df = pd.DataFrame(
    #     columns=["pclass", "name", "sex", "age", "sibsp", "parch", "fare", "cabin", "embarked"],
    #     data=[[pclass, name, sex, age, sibsp, parch, fare, cabin, embarked]]
    # )
    data=[[pclass, name, sex, age, sibsp, parch, fare, cabin, embarked]]

    pipeline = load('model/titanic_pipeline.joblib')
    scaler = load('model/scaler.joblib')

    X = tfunc.clean_df(data).values
    X = scaler.transform(X)
    y_pred_log = pipeline.predict(X)
    y_pred = y_pred_log[0]

    msg = ""

    if y_pred == 0:
        msg = "You would have not survived :("
    elif y_pred == 1:
        msg = "Congratulations! You would have survived the Titanic"
    else:
        msg = "Sorry, something went wrong."

    return msg