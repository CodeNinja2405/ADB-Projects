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


connection = sqlite3.connect('data2.db', check_same_thread= False)
cursor = connection.cursor()

app = Flask(__name__)




@app.route("/")
def hello_world1():
    return render_template('index.html')


@app.route('/taskone', methods=['GET', 'POST'])
def hello_world():
    fruits_dict = {}
    count_fruits = int(request.form['fruits'])
    fruitnames_withlmiter = request.form['fruitsname']
    fruitnames = fruitnames_withlmiter.split(',')
    for i in range(count_fruits):
        cursor.execute(
            "SELECT COUNT(*) FROM data2 WHERE column4 = '" + fruitnames[i]+"'")
        count = cursor.fetchone()[0]
        fruits_dict[fruitnames[i]] = count

    return render_template('taskone.html', data=fruits_dict)


@app.route('/tasktwo', methods=['GET', 'POST'])
def hello_world2():
    list = ()
    fruits_dict = {}
    fruitsl = (request.form['fruitsl'])
    cursor.execute(
        "SELECT column4,COUNT(*) AS NUMBER FROM data2 GROUP BY column4 ORDER BY NUMBER DESC LIMIT " +fruitsl)
    list = cursor.fetchall()
    for i in range(int(fruitsl)):
        fruits_dict[list[i][0]] = list[i][1]
    print(fruits_dict)
    return render_template('tasktwo.html', data=fruits_dict)


@app.route('/taskthree', methods=['GET', 'POST'])
def hello_world3():
    column1 = []
    column2 = []
    if request.method == 'POST':
        low_range = request.form['lowrange']
        high_range = request.form['highrange']
        query = "select column1, column3 from data2 WHERE column1 BETWEEN " + low_range + " AND " + high_range
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        for i in data:
            column1.append(i[0])
            column2.append(i[1])
        print(column1)
        print(column2)

    return render_template('taskthree.html', col1=column1, col2=column2)


if(__name__) == "__main__":
    app.run()

