from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, send_file
import requests
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# dataset load
df = pd.read_csv('bank-full.csv',';')
df.drop(columns='day month poutcome y'.split(), inplace=True)

# model load
model = joblib.load('svm_model_final')

app = Flask(__name__)

# sql database connection initiation
sqldb = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password = '1a2d3g4j'
)

c = sqldb.cursor(buffered=True)
query = 'USE bank_final_project'
c.execute(query)

@app.route('/', methods=['GET'])
def start():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def home():
    bank = request.form

    age = int(bank['age'])
    job = bank['job']
    marital = bank['marital']
    education = bank['education']
    default = bank['default']
    balance = float(bank['balance'])
    housing = bank['housing']
    loan = bank['loan']
    contact = bank['contact']
    duration = int(bank['duration'])
    campaign = int(bank['campaign'])
    pdays = int(bank['pdays'])
    previous = int(bank['previous'])

    data_input=[[age, job, marital, education, default, balance, housing, loan, contact, duration, campaign, pdays, previous]]

    # df_test = pd.DataFrame(data_input, columns = df.columns, index=[0])
    # pred = model.predict(df_test)
    pred=0.57

    query= f'''INSERT INTO `customers` VALUES ({age}, '{job}','{marital}','{education}','{default}','{balance}', '{housing}', '{loan}', '{contact}', {duration}, {campaign}, {pdays}, {previous}, (SELECT CURDATE()));'''
    print(query)
    c.execute(query)
    sqldb.commit()

    return render_template('predict.html', data=pred)

if __name__ == "__main__":
    app.run(debug=True)