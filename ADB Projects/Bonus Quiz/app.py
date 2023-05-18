# from distutils.log import debug
# from select import select
# from colorama import Cursor
from flask import Flask, render_template, request, url_for
import sqlite3
import pyodbc
# from werkzeug.utils import secure_filename
# import os
# import random
# from werkzeug.utils import redirect
# from werkzeug.utils import redirect

# connection = sqlite3.connect('class.db', check_same_thread= False)
# cursor = connection.cursor()


# cursor = pyodbc.connect(driver='{SQL Server}', host='adbixm6153.database.windows.net', database='Assign_0_Database',
                    #   trusted_connection='no', user='ixm6153', password='fQQ3L?HN!T6Drtzt')


# cursor = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', host='adbixm6153.database.windows.net', database='Assign_0_Database',
#                       trusted_connection='no', user='ixm6153', password='fQQ3L?HN!T6Drtzt')


connection = sqlite3.connect('data3.db', check_same_thread= False)
cursor = connection.cursor()

app = Flask(__name__)






@app.route("/")
def hello_world1():
    return render_template('index.html')


@app.route('/index', methods=['POST', 'GET'])
def hello_world():
    dict = {}
    list = ()
    input_names = request.form['names']
    names = input_names.split(' ')
    type = request.form['oddeven']
    if(type == 'odd'):
        type = '1'
    else:
        type = '0'
    for i in range(len(names)):
        cursor.execute(
            "SELECT count(*) FROM data3 WHERE field2 ='" +
            names[i] + "' and field1 % 2="+type
        )
        list = cursor.fetchall()
       
        print(list[0][0])
        dict[names[i]] = list[0][0]
    print(dict)
    return render_template('task1.html', data=dict)


if __name__ == "__main__":
    app.run()