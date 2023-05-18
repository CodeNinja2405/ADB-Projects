from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/searchName')
def searchName():
   return render_template('searchName.html')
@app.route('/updateKeyword')
def updateKeyword():
   return render_template('updateKeyword.html')
@app.route('/updateSalary')
def updateSalary():
   return render_template('updateSalary.html')

@app.route('/deleteRecord')
def deleteRecord():
   return render_template('deleteRecord.html')

@app.route('/addNewRecord')
def addNewRecord():
   return render_template('addNewRecord.html')

@app.route('/salaryRange')
def salaryRange():
   return render_template('salaryRange.html')

@app.route('/addImage')
def addImage():
   return render_template('addImage.html')

import sqlite3
@app.route('/table', methods=['POST','GET'])
def fulllist():
    #connecting toSQLite
    connecttosql = sqlite3.connect('dataset1.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    # executing the query
    cursor.execute("Select * from data1 ")
    #fetching the values
    result = cursor.fetchall()
    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("list.html",rows = result)

@app.route('/namesearch', methods=['POST','GET'])
def name():
    #connecting to SQLite
    connecttosql = sqlite3.connect('dataset1.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    value=request.form['Keyword']
     # executing the query
    cursor.execute("Select * from data1  WHERE Keywords = '"+value+"' ") 
    # cursor.execute("Select * from data1 where keywords in ANY (select keywords from data1 WHERE Keywords = '"+value+"') ") 
    #fetching the values
    result = cursor.fetchall()
    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("list.html",rows = result)


@app.route('/addpicture',methods=['POST','GET'])
def addimg():
    if (request.method=='POST'):
         #connecting to SQLite
        connecttosql = sqlite3.connect('dataset1.db')
        #creating a cursor
        cursor = connecttosql.cursor()
        # executing the query
        Telnumber=request.form['Telnum']
        image= request.form['Image']
        # personname= request.form['Name']
        cursor.execute("UPDATE data1 SET Picture = '"+image+"'  WHERE Num ='"+Telnumber+"' ")
        connecttosql.commit()
        # executing the query
        cursor.execute("Select * from data1 ")
        #fetching the values
        result = cursor.fetchall()
        #closing the connection to SQLite
        connecttosql.close()
        #returning the result
    return render_template("list.html",rows = result)


@app.route('/namedelete', methods=['GET', 'POST'])
def deleterecord():
    if (request.method=='POST'):
         #connecting to SQLite
        connecttosql = sqlite3.connect('dataset1.db')
        #creating a cursor
        cursor = connecttosql.cursor()
        personname= request.form['Name']
        # executing the query
        cursor.execute("DELETE FROM data1 WHERE Name ='"+personname+"' ")
        connecttosql.commit()
        # executing the query
        cursor.execute("Select * from data1 ")
        #fetching the values
        result = cursor.fetchall()
        #closing the connection to SQLite
        connecttosql.close()
        #returning the result
    return render_template("list.html",rows = result)

@app.route('/sal', methods=['GET', 'POST'])
def salrng():
    if (request.method=='POST'):
         #connecting to SQLite
        connecttosql = sqlite3.connect('dataset1.db')
        #creating a cursor
        cursor = connecttosql.cursor()
        # executing the query
        minimum= request.form['min']
        maximum= request.form['max']
        query1="Select * from data1 WHERE cast(Num as double) BETWEEN @min AND @max and Num is not null and trim(Num)!=''"
        # executing the query
        cursor.execute(query1,{'min':minimum,'max':maximum})
        #fetching the values
        result = cursor.fetchall()
        #closing the connection to SQLite
        connecttosql.close()
        #returning the result
    return render_template("list.html",rows = result)

@app.route('/addperson', methods=['GET', 'POST'])
def addper():
    if (request.method=='POST'):
         #connecting to SQLite
        connecttosql = sqlite3.connect('dataset1.db')
        #creating a cursor
        cursor = connecttosql.cursor()
        # executing the query
        Name= request.form['Name']
        Picture= request.form['Image']
        Telnum= request.form['Telnum']
        Keywords= request.form['Keyword']
        # executing the query
        cursor.execute("INSERT INTO data1 VALUES ('"+Name+"','"+Picture+"','"+Telnum+"','"+Keywords+"')")
        connecttosql.commit()
        # executing the query
        cursor.execute("select * from data1 ")
        #fetching the values
        result = cursor.fetchall()
        #closing the connection to SQLite
        connecttosql.close()
        #returning the result
    return render_template("list.html",rows = result)

if __name__ == '__main__':
    app.run()
    