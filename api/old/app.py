from joblib import load
import numpy as np
import os
import flask
from flask import request, jsonify
import titanic_functions as tfunc

#os.chdir("./api")


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Titanic API</h1>
<p>A project for practising Restful API in Machine Learning models</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/', methods=['GET', 'POST'])
def make_prediction():
    data = request.get_json()
    X = tfunc.clean_df(data).values
    print(X)

    prediction = str(pipeline.predict(X)[0])
    print(type(prediction))
    print(prediction)

    return prediction
    

if __name__ == '__main__':
    pipeline = load('./pipeline_model/titanic_pipeline.joblib')


app.run(debug=True)
