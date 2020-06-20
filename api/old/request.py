import requests
import json

url = 'http://127.0.0.1:5000/api/v1/'

data = [[1, "Andrews, Mr. Thomas Jr", "male",39.0,0,0,0.0,"A36","S"]]

j_data = json.dumps(data)
print(j_data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)
