
import json
import numpy as np
import os
import joblib

def init():
    global model
    global scaler
    model_path = './model_folder/titanic-api-model.pkl'
    model = joblib.load(model_path)

    scaler_path = './model_folder/titanic-api-scaler.pkl'
    scaler = joblib.load(scaler_path)

###### POWER BI ######

# providing 3 sample inputs for schema generation
standard_sample_input = StandardPythonParameterType([1, "Raul", "male", 25, 0, 0, 300, "C32", "S"])

# This is a nested input sample, any item wrapped by `ParameterType` will be described by schema
sample_input = StandardPythonParameterType({'input1': standard_sample_input})

#sample_global_parameters = StandardPythonParameterType(1.0) #this is optional
sample_output = StandardPythonParameterType([1.0])

@input_schema('inputs', sample_input)
#@input_schema('global_parameters', sample_global_parameters) #this is optional
@output_schema(sample_output)


######################


def run(data):

    #ws = Workspace(subscription_id="fc1c5e68-95c2-4bce-9ff9-5bd8442fb921", resource_group="titanic-api", workspace_name="titanic-ws")

    try:
        data = json.loads(data)['data']
        data = scaler.transform([data])
        result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
