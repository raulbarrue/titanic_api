import os
from joblib import load
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

import titanic_functions as tfunc

app = Flask(__name__)
CORS(app)
api = Api(app)# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("pclass", type="int64")
parser.add_argument("name")
parser.add_argument("sex")
parser.add_argument("age", type="int64")
parser.add_argument("sibsp", type="int64")
parser.add_argument("parch", type="int64")
parser.add_argument("fare", type="int64")
parser.add_argument("cabin")
parser.add_argument("embarked")

# Unpickle our model so we can use it!
pipeline = load('./pipeline_model/titanic_pipeline.joblib')

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        # Sklearn is VERY PICKY on how you put your values in...
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


        _y = pipeline.predict(X)[0]
        return {"class": _y}

api.add_resource(Predict, "/predict")

if __name__ == "__main__":
    app.run(debug=True)