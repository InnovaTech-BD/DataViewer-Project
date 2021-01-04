from __future__ import print_function
from flask import Flask, render_template
from IPython.display import HTML
from googleapiclient.discovery import build
from google.oauth2 import service_account


import pandas as pd
import numpy as np

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

arr = np.arange(4, 2, 4)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1xl0OP_IhryWg4eXU5F8K6GoFVDKe0gpdNo5u13WjLlI'
SAMPLE_RANGE_NAME = 'Sheet2!A1:Z1000'

SERVICE_ACCOUNT_FILE = 'cherie-notebook-cred.json'  # just need to redefine this

credentials = None
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()


data = result['values']
numRows = len(data)

for i in range(1, numRows):
    data[i].append("n/a")

numCols = len(data[0])

columns = []
datarows = np.empty([numRows - 1, numCols], dtype=object)

for column in data[0]:  # column names
    columns.append(column.strip())

for i in range(numRows):
    if i == 0:
        continue
    else:
        for j in range(numCols):
            datarows[i - 1][j] = data[i][j]

dataframe = pd.DataFrame(data=datarows, columns=columns)


dd = HTML(dataframe.to_html(classes='table table-striped table-hover'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/order")
def order():
    return render_template('order.html', title='Orders', data=dd)


@app.route("/customer_list")
def customer_list():
    return render_template('customer_list.html', title='Customers List')



