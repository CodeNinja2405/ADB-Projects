from flask import Flask,render_template,request
from time import time
import pyodbc
import urllib.parse
import redis
import hashlib
import pickle

app = Flask(__name__)

@app.route('/')
def MainHome():
    return render_template('index.html')


conn = pyodbc.connect(driver='{SQL Server}', host='adbixm6153.database.windows.net', database='Assign_0_Database',
                      trusted_connection='no', user='ixm6153', password='fQQ3L?HN!T6Drtzt')

# conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', host='adbixm6153.database.windows.net', database='Assign_0_Database',
#                       trusted_connection='no', user='ixm6153', password='fQQ3L?HN!T6Drtzt')


r = redis.StrictRedis(host='ixm6153red.redis.cache.windows.net',port=6380, db=0, password='rFobmUhZvsFdfpoMT2tOkBxevcrDEn0oFAzCaEdcxHc=', ssl=True)

cursor = conn.cursor()





@app.route("/queryone" , methods=['GET','POST'])
def firstquestion():
    starttime = time()
    

    syr1 = str(request.args.get('y1'))
    eyr2 = str(request.args.get('y2'))
    svt1 = str(request.args.get('v1'))
    evt2 = str(request.args.get('v2'))

    cursor.execute("Select TOP 5 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"   ;")
    rows = cursor.fetchall()

    #Max to min
    cursor.execute("Select TOP 1 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes DESC ;")
    maxitomin = cursor.fetchall()
    #Min to max
    cursor.execute("Select TOP 1 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes  ;")
    mintomax = cursor.fetchall()
    
    # cursor.execute("select * from pvotes ;")
    # clusterrows = cursor.fetchall()

    endtime = time()
    timediff = endtime - starttime
    return render_template("list.html",setdetails = timediff,drows = rows,erows=maxitomin,frows=mintomax)


@app.route("/withfor" , methods=['GET','POST'])
def withfor1():
  
  syr1 = str(request.args.get('y1'))
  eyr2 = str(request.args.get('y2'))
  svt1 = str(request.args.get('v1'))
  evt2 = str(request.args.get('v2'))


  getnum = str(request.args.get('fnum'))
  starttime = time()
  for x in range(int(getnum)):
  #  cursor.execute("select time, latitude, longitude, mag,id, place from earthquake where mag >3.5;")
   cursor.execute("Select TOP 5 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"   ;")
   rows = cursor.fetchall()
   cursor.execute("Select TOP 1 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes DESC ;")
   maxitomin = cursor.fetchall()
   cursor.execute("Select TOP 1 * from pvotes  where year between "+str(syr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes  ;")
   mintomax = cursor.fetchall()
    
    

 #rows = cursor.fetchall()
  endtime = time()
  timediff = endtime - starttime
  # return render_template('secondquery.html', settimebefore=starttime, settimeafter=endtime, settime=timediff)
  return render_template("list.html",setdetails = timediff,drows = rows,erows=maxitomin,frows=mintomax)








@app.route("/withredis" , methods=['GET','POST'])
def withredis1():
  
  result = r.ping()
  print("Ping returned : " + str(result))
  getRandom=str(request.args.get('loopiteration'))
  
  syrr1 = str(request.args.get('y1'))
  eyr2 = str(request.args.get('y2'))
  svt1 = str(request.args.get('v1'))
  evt2 = str(request.args.get('v2'))
  
  # query= "select time,mag,id, place from earthquake where mag = 5.8;"
  query1= "Select TOP 5 * from pvotes  where year between "+str(syrr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"   ;"
  
  #Max
  query2= "Select TOP 5 * from pvotes  where year between "+str(syrr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes DESC ;"
  
  #Min
  query3= "Select TOP 5 * from pvotes  where year between "+str(syrr1)+" and "+str(eyr2)+" and votes between "+str(svt1)+" and "+str(evt2)+"  ORDER BY votes  ;"


  hash = hashlib.sha224(query1.encode('utf-8')).hexdigest()
  key = "redis_cache:" + hash
  starttime=time()
  for i in range(int(getRandom)):
    if (r.get(key)):
      print("redis cached")
    else:
      print(key)
      print(r)
      cursor.execute(query1)
      rows = cursor.fetchall()
      r.expire(key, 36)

    cursor.execute(query1)
    rows = cursor.fetchall()
  
  
  cursor.execute(query2)
  maxitomin = cursor.fetchall()
  cursor.execute(query3)
  mintomax = cursor.fetchall()
  
  
  endtime = time()
  executiontime = endtime - starttime
  return render_template("list.html",setdetails = executiontime,drows = rows, erows=maxitomin, frows=mintomax)




if __name__ == '__main__':
    app.run()


