import serial
from time import sleep
import MySQLdb
Ser = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
Counter = 1
db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
#con=MySQLdb.connect(host="localhost", user="root", passwd="iiits123", db="Weather")
cur = db.cursor()

while Counter:
    data = Ser.readline()
    print(data)
    ind=data.find('%')
    if ind>0:
    	humidity=data[0:ind]
    	ind1=data.find('c')
    	temperature=data[ind+2:ind1]
    	print humidity
    	print temperature
    	print ind	
    	cur.execute('''select count(*) from Weather''')
    	count=cur.fetchone()[0]
    	count=int(count)
    	count=count+1
    	cur.execute('''INSERT INTO Weather(id,Humidity,Temperature) values(%s, %s, %s)''',(count,humidity,temperature))
    	db.commit();
    sleep(1)
Ser.close()
