from distutils.log import debug
from select import select
from flask import Flask, render_template, request
import sqlite3
from werkzeug.utils import secure_filename
import os
import random
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect



app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')
 
sqlconnection = sqlite3.connect('class.db', check_same_thread= False)
sqlcursor = sqlconnection.cursor()

sqlconnection1 = sqlite3.connect('students.db', check_same_thread= False)
sqlcursor1 = sqlconnection1.cursor()



SName = ''
AName = ''


@app.route("/index", methods=['GET', 'POST'])
def Home():
    global SName
    global AName

    if request.method == 'POST':
        Name = str(request.form['Name'])
        select = request.form['select']

        
        if select=='Student':
            SName=Name
            t1query = "select * from class;"
            sqlcursor.execute(t1query)
            rows = sqlcursor.fetchall()
            return render_template('student.html', frows = rows)

        if select=='Admin':
            AName=Name
            SName=Name
            t1query = "select * from class;"
            sqlcursor.execute(t1query)
            rows = sqlcursor.fetchall()
            t2query = "select * from students;"
            sqlcursor1.execute(t2query)
            rows2 = sqlcursor1.fetchall()

            return render_template('admin.html', frows = rows, frows2 = rows2)

    else:
      return render_template('home.html')


# @app.route("/stud", methods=['GET', 'POST'])
# def StudentPage():
#     global SName
#     global AName

#     t1query = "select * from class;"
#     sqlcursor.execute(t1query)
#     rows = sqlcursor.fetchall()
#     # t12query = "select count(*) as Num_of_Earthquakes from all_month where mag > "+getmag+";"
#     # sqlcursor.execute(t12query)
#     # count = sqlcursor.fetchall()
#     return render_template('student.html', frows = rows)
    


    



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

