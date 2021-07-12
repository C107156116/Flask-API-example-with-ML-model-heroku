# -*- coding: utf-8 -*-
import numpy as np
import pickle
import pandas as pd
from flask import Flask, jsonify,request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/test')
def userin():
     return 'hello!!'
@app.route('/rate',methods=['POST'])
def postInput():
     # 取得前端傳過來的值
     inserValues=request.get_json()
     cols =['Age','DailyRate','Department','DistanceFromHome','Education','EducationField','EmployeeNumber','EnvironmentSatisfaction','Gender','HourlyRate','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MaritalStatus','MonthlyIncome','MonthlyRate','NumCompaniesWorked','OverTime','PercentSalaryHike','PerformanceRating','RelationshipSatisfaction','StockOptionLevel','TotalWorkingYears','TrainingTimesLastYear','WorkLifeBalance','YearsAtCompany','YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager']
     data_2=['41','1102','Sales','1','2','Life Sciences','1','2','Female','94','3','2','Sales Executive','4','Single','5993','19479','8','Yes','11','3','1','0','8','0','1','6','4','0','5']

     data=[]
     process_data=[]
     act=[]
     input_data=[]

     raw_df = pd.read_excel("WA_Fn-UseC_-HR-Employee-Attrition_Data_First_Processes_SMOTE_2.xls")
     raw_df =raw_df[cols]

     for i in range(0,len(cols),1):
          data.append(inserValues[cols[i]])
     bus=inserValues['BusinessTravel']
     de={'Sales':0,'Research & Development':1,'Human Resources':2}
     data[2]=de[data[2]]

     edu={'Life Sciences':0,'Medical':1,'Marketing':2,'Technical Degree':3,'Human Resources':4,'Other':5}
     data[5]=edu[data[5]]

     gen={'Female':0,'Male':1}
     data[8]=gen[data[8]]

     job_roel={'Sales Executive':0,'Research Scientist':1,'Laboratory Technician':2,'Manufacturing Director':3,'Healthcare Representative':4,'Manager':5,'Sales Representative':6,'Research Director':7,'Human Resources':8}
     data[12]=job_roel[data[12]]

     mar={'Divorced':0,'Single':1,'Married':2}
     data[14]=mar[data[14]]

     over_time={'Yes':0,'No':1}
     data[18]=over_time[data[18]]
     
     for i in range(0,len(cols),1):   
          max_num=max(raw_df[cols[i]])
          min_num=min(raw_df[cols[i]])
          pro_num=round(((float(data[i])-min_num)/(max_num-min_num)),16)
          process_data.append(pro_num)
     if bus == 'Non-Travel':
          process_data.append(float(1))
          process_data.append(float(0))
          process_data.append(float(0))
     elif bus == 'Travel_Frequently':
          process_data.append(float(0))
          process_data.append(float(1))
          process_data.append(float(0))
     elif bus == 'Travel_Rarely':
          process_data.append(float(0))
          process_data.append(float(0))
          process_data.append(float(1))
     input_data.append(process_data)
     process_data=[]
     data=[]
     
     pickle_in = open('randomforest.pickle','rb')
     forest = pickle.load(pickle_in)
     print(input_data)
     predict_rate=forest.predict_proba(input_data)
     predict_result = forest.predict(input_data)
     print(predict_result)

     print(data)
     return jsonify({'predict_result':str(predict_result[0]),'Turnover_rate':str(predict_rate[0][1])})
