import os
from joblib import load
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
import sys
#sys.path.append('/DS Projects/titanic_api/lib/')

import titanic_functions as tfunc


app = Flask(__name__)
CORS(app)
api = Api(app)

# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("pclass")
parser.add_argument("name")
parser.add_argument("sex")
parser.add_argument("age")
parser.add_argument("sibsp")
parser.add_argument("parch")
parser.add_argument("fare")
parser.add_argument("cabin")
parser.add_argument("embarked")

# Unpickle our model so we can use it!
pipeline = load('./pipeline_model/titanic_pipeline.joblib')
sc = load("./pipeline_model/scaler.joblib")

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        X = ([[
            args["pclass"],
            args["name"],
            args["sex"],
            args["age"],
            args["sibsp"],
            args["parch"],
            args["fare"],
            args["cabin"],
            args["embarked"]
            ]])
        X = tfunc.clean_df(X).values
        X = sc.transform(X)

        y = pipeline.predict(X)[0]
        
        #return {"class": str(y)}

        if y == 0:
            msg = "DIE :("
        elif y == 1:
            msg = "SURVIVE :)"
        else:
            msg = "Something went wrong"
            
        return {"class": str(msg)}

api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    app.run(debug=True)