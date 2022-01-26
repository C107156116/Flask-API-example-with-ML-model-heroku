from black import re
from itsdangerous import encoding
import numpy as np
import pickle
import pandas as pd
import json
import heapq
from flask import Flask, jsonify,request
from flask_cors import CORS
from json import dumps
from flask import Flask, make_response
app = Flask(__name__)
CORS(app)
data=pd.read_csv('test.csv',encoding='unicode_escape')
@app.route('/HelloWord')
def hello_world():
     try:
          return 'HelloWord'
     except Exception as e:
          print(e)
          return '500'
@app.route('/supervisor_chart')
def supervisor_chart():
     try:
          data=pd.read_csv('supervisor_2020_2021.csv',encoding='utf-8')
          js = data.to_dict(orient="records")
          return make_response(dumps(js))
     except Exception as e:
          print(e)
          return '500'
@app.route('/post_example',methods=['POST'])
def post_example():
     try:
          inserValues=request.get_json()
          print(inserValues['DATAYEAR_LAST'])
          out_data=data(data['DATAYEAR_LAST']==(inserValues['DATAYEAR_LAST']))
          return make_response(dumps(out_data))
     except Exception as e:
          print(e)
          return 'Server 500'
@app.route('/get_home_data')
def get_home_data():
     try:
         data_col=['EMPLOYEE_ID','LOCATION_CODE_LAST','DEPARTMENT_ID_LAST','JOB_DESC_NEW','IS_ALIVE_LAST']
         data_out=data[data_col]
         print(data_out)
         data_out=data_out.head(2000)
         js = data_out.to_dict(orient="records")
         return make_response(dumps(js))
     except Exception as e:
          print(e)
          return '500'
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
