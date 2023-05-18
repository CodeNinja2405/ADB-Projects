from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

import sqlite3
@app.route('/table', methods=['POST','GET'])
def fulllist():
    #connecting toSQLite
    connecttosql = sqlite3.connect('data.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    # executing the query
    cursor.execute("Select * from earth")
    #fetching the values
    result = cursor.fetchall()
    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("list.html",rows = result)

#Question 10
#earthquakes within that area
@app.route("/quakes")
def quakesnear():
    return render_template("quakes.html")
@app.route("/quakes", methods=["GET", "POST"])
def nearbyquakes():
    #connecting toSQLite
    connecttosql = sqlite3.connect('data.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    # executing the query
    cursor.execute("select * from earth")
    result2=cursor.fetchall()
    latitude1 =request.form['lat1']
    longitude1 = request.form['lon1']
    latitude2 = request.form['lat2']
    longitude2 = request.form['lon2']
   # print (lat1)
    cursor.execute("select time, latitude, longitude, id, place from earth where latitude >= "+latitude1+" and latitude <= "+latitude2+" and longitude >= "+longitude1+" and longitude <= "+longitude2+" ;")
    result = cursor.fetchall()
    connecttosql.close()   
    return render_template("quakes.html", rows=result, count=len(result))
    
  #Question 11  
@app.route("/inRange")
def quakesinrange():
    return render_template("quakesInRange.html")

#Earthquakes with in the given range 
import sqlite3
@app.route('/inRange', methods=['POST','GET'])
def inrange():
    #connecting toSQLite
    connecttosql = sqlite3.connect('data.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    minimum = request.form['min']
    maximum = request.form['max']
    net=request.form['net']
    # executing the query
    cursor.execute("Select time, latitude, longitude, id, place from earth where (mag between '"+minimum+"' and '"+maximum+"') and (net = '"+net+"') order by mag desc limit 5")
    #fetching the values
    result = cursor.fetchall()
    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("quakesInRange.html",rows = result,count=len(result))   


#Question  12
@app.route("/task3")
def task3():
    return render_template("task3.html")
import sqlite3
@app.route('/task3', methods=['POST','GET'])
def task03():
    #connecting toSQLite
    connecttosql = sqlite3.connect('data.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    From=request.form['date1']

    to=request.form['date2']
    # executing the query
    cursor.execute("select time from earth")
    result = cursor.fetchall()
    # cursor.execute("Select time, latitude, longitude, id, place,net,count(net) from earth where time between '"+From+"' and '"+to+"'group by net  order by count(net)")
    cursor.execute("select time, latitude, longitude, id, place,net, min(cnt) netCount  from  (Select time, latitude, longitude, id, place,net,count(net) as cnt from earth e where time between '"+From+"' and '"+to+"' group by net)")
    result = cursor.fetchall()
    # cursor.execute("select *  from earth where (SUBSTRING(time,12,12)>'20:00:00.000' or SUBSTRING(time,12,12)<'06:00:00.000') and mag > 4.0 and type= 'earthquake' ")
    cursor.execute("select time, latitude, longitude, id, place,net, max(cnt) netCount  from  (Select time, latitude, longitude, id, place,net,count(net) as cnt from earth e where time between '"+From+"' and '"+to+"' group by net)")
    #fetching the values
    result2 = cursor.fetchall()

    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("task3.html",rows = result, rows2=result2)  


#question13
@app.route("/task4")
def update1():
    return render_template("task4.html")

#Earthquakes with in the given range 
import sqlite3
@app.route('/task4', methods=['POST','GET'])
def update():
    #connecting toSQLite
    connecttosql = sqlite3.connect('data.db')
    #creating a cursor
    cursor = connecttosql.cursor()
    net1=request.form['net1']
    net2=request.form['net2']
    # executing the query
    cursor.execute("select * from earth where net = 'nn' ")
    result2=cursor.fetchall()
    cursor.execute("UPDATE earth SET net = '"+str(net2)+"'   WHERE net ='"+str(net1)+"' ")
    # result = cursor.fetchall()
    result = cursor.rowcount
    #closing the connection to SQLite
    connecttosql.close()
    #returning the result
    return render_template("task4.html",count = result)   


if __name__ == '__main__':
    app.run()