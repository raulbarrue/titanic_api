from joblib import load
import pandas as pd
import numpy as np
import os

import titanic_functions as tfunc



# model = load('./modelling/outcomes/voting_classifier_titanic.joblib')
# sc = load("./modelling/outcomes/scaler.joblib")

####### OPTION 1 ###########

# #X = df2.drop(["survived"], axis=1).iloc[7]
# X = np.array([1., 39.,  0.,  0.,  0.,  1.,  0.,  1., 39.,  0.,  1.,  0.,  0., 1.,  0.,  0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.])

# X = sc.transform(X.reshape(1,-1))

# pred = model.predict(X)

# print("Prediction:", pred)

####### OPTION 2 ###########

# input_x = [1, "Andrews, Mr. Thomas Jr", "male",39.0,0,0,0.0,"A36","S"]



##################################################################
####################### TEST #####################################
##################################################################

def process_input(x):
    return [1., 39.,  0.,  0.,  0.,  1.,  0.,  1., 39.,  0.,  1.,  0.,  0., 1.,  0.,  0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.]

def test_input():
    expected_output = [1., 39.,  0.,  0.,  0.,  1.,  0.,  1., 39.,  0.,  1.,  0.,  0., 1.,  0.,  0.,  1.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.]
    
    user_input = [[1, "Andrews, Mr. Thomas Jr", "male",39.0,0,0,0.0,"A36","S"]]
    
    X = tfunc.clean_df_one_observation(user_input)
    
    assert process_input(X) == expected_output

def test_prediction():

    ############# MANUAL INPUT - THE ERROR IS IN THE STANDARDSCALER DECIMALS

    # expected_output = 0
    # user_input = [[1, "Andrews, Mr. Thomas Jr", "male",39.0,0,0,0.0,"A36","S"]]
    
    # model = load('../modelling/outcomes/voting_classifier_titanic.joblib')
    # sc = load("../modelling/outcomes/scaler.joblib")

    # X = tfunc.clean_df_one_observation(user_input)
    # X = sc.transform(X.values.reshape(1,-1))

    # '''THE BUG IS IN THE DECIMALS!!!!!!!!!!!!!!'''

    # y_pred = model.predict(X)

    # assert y_pred == expected_output

    ############# PANDAS INPUT
    model = load('../modelling/outcomes/voting_classifier_titanic.joblib')
    sc = load("../modelling/outcomes/scaler.joblib")

    df2 = pd.read_csv("../dataset/titanic_data.csv").drop(["boat", "survived", "body", "home.dest", "ticket"], axis=1)
    df2 = tfunc.clean_df(df2)

    expected_output = 0
    user_input = [df2.iloc[7].values]

    #X = tfunc.clean_df_one_observation(user_input)
    X = sc.transform(user_input)

    y_pred = model.predict(X)

    assert y_pred == expected_output

    # Notes:
    #  - If first get single input values, then process columns, then transform --> Doesn't work.
    #  - If first get clean_df (process columns), then get single input value, then transform --> It works


    ############# EXPERIMENT
    # expected_output = 0
    # user_input_raw = [[1, "Andrews, Mr. Thomas Jr", "male",39.0,0,0,0.0,"A36","S"]]
    # model = load('../modelling/outcomes/voting_classifier_titanic.joblib')
    # sc = load("../modelling/outcomes/scaler.joblib")

    # df2 = pd.DataFrame(user_input_raw, columns = ["pclass", "name", "sex", "age", "sibsp", "parch", "fare", "cabin", "embarked"])
    # df2 = tfunc.clean_df(df2)


    # user_input = df2.values
    # #X = tfunc.clean_df_one_observation(user_input)
    # X = sc.transform(user_input)

    # y_pred = model.predict(X)

    # assert y_pred == expected_output