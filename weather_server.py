from flask import Flask, session, redirect, url_for, request, render_template
app = Flask(__name__)
import sys
import subprocess 
import MySQLdb
import re 
import os 
import time 
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cookielib
import urllib2
from getpass import getpass
import stat
import geocoder
import json
from itertools import chain
from twilio.rest import TwilioRestClient
#db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
#cur = db.cursor()




@app.route('/')
def home():
	return redirect(url_for('index'))



@app.route('/index')
def index():
	print "hai"
	db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
	cur = db.cursor()
	cur.execute('''select count(*) from Weather''')
	count=cur.fetchone()[0]
	print count
	cur.execute("SELECT Humidity FROM Weather WHERE id = %s;", [count])
	humidity=cur.fetchone()[0]
	cur.execute("SELECT Temperature FROM Weather WHERE id = %s;", [count])
	temperature=cur.fetchone()[0]
	cur.close()
	chennai=geocoder.google('Chennai')
	hyderabad=geocoder.google('Hyderabad')
	visakhapatnam=geocoder.google('Visakhapatnam')
	vijayawada=geocoder.google('Vijayawada')
	chennailat=str(chennai.lat)
	chennailon=str(chennai.lng)
	hydlat=str(hyderabad.lat)
	hydlon=str(hyderabad.lng)
	vskplat=str(visakhapatnam.lat)
	vskplon=str(visakhapatnam.lng)
	bzalat=str(vijayawada.lat)
	bzalon=str(vijayawada.lng)

	url1="http://api.openweathermap.org/data/2.5/weather?lat="+chennailat+"&lon="+chennailon+"&APPID=1b7843ebea1f3c96215fb1a374e6e1b6"
	url2="http://api.openweathermap.org/data/2.5/weather?lat="+hydlat+"&lon="+hydlon+"&APPID=1b7843ebea1f3c96215fb1a374e6e1b6"
	url3="http://api.openweathermap.org/data/2.5/weather?lat="+vskplat+"&lon="+vskplon+"&APPID=1b7843ebea1f3c96215fb1a374e6e1b6"
	url4="http://api.openweathermap.org/data/2.5/weather?lat="+bzalat+"&lon="+bzalon+"&APPID=1b7843ebea1f3c96215fb1a374e6e1b6"
	#chennai
	res = urllib2.urlopen(url1)
	a= res.read()
	a1 = a.replace("'", "\"")
	html= json.loads(a1)
	chum=html['main']['humidity']
	temperature1=float(html['main']['temp'])-273
	ctemp=str(temperature1)
	speed1=float(html['wind']['speed'])*1.609
	cspeed=str(speed1)
	#vizag
	res2 = urllib2.urlopen(url3)
	b= res2.read()
	b1 = b.replace("'", "\"")
	html2= json.loads(b1)	
	vskphum=html2['main']['humidity']
	temperature2=float(html2['main']['temp'])-273
	vskptemp=str(temperature2)
	speed2=float(html2['wind']['speed'])*1.609
	vspeed=str(speed2)
	#hyderabad
	res3 = urllib2.urlopen(url2)
	c= res3.read()
	c1 = c.replace("'", "\"")
	html3= json.loads(c1)	

	hydhum=html3['main']['humidity']
	temperature3=float(html3['main']['temp'])-273
	hydtemp=str(temperature3)
	speed3=float(html3['wind']['speed'])*1.609
	hspeed=str(speed3)
	#vijayawada
	res4 = urllib2.urlopen(url4)
	d= res4.read()
	d1 = d.replace("'", "\"")
	html4= json.loads(d1)	

	bzahum=html4['main']['humidity']
	temperature4=float(html4['main']['temp'])-273
	bzatemp=str(temperature4)
	speed4=float(html4['wind']['speed'])*1.609
	bspeed=str(speed4)
	return render_template('index.html',humidty=humidity,temperature=temperature,chum=chum,ctemp=ctemp,vskph=vskphum,vskptemp=vskptemp,hydh=hydhum,hydtemp=hydtemp,bzah=bzahum,bzatemp=bzatemp,cs=cspeed,vs=vspeed,hs=hspeed,bs=bspeed)



@app.route('/maps')
def maps():
	db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
	cur = db.cursor()
	cur.execute('''select count(*) from Weather''')
	count=cur.fetchone()[0]
	print count
	cur.execute("SELECT Humidity FROM Weather WHERE id = %s;", [count])
	humidity=cur.fetchone()[0]
	k=str(humidity)
	k=k+"%"
	print type(k)
	print k
	cur.execute("SELECT Temperature FROM Weather WHERE id = %s;", [count])
	temperature=cur.fetchone()[0]
	j=str(temperature)
	
	print type(j)
	print j
	weat="Temperature : "+j+"degrees\nHumidity : "+k+"%"
	cur.close()
	li=[]
	li.append(k)
	li.append(j)
	print weat
	return render_template('maps.html',weat=weat,li=li)

'''@app.route('/sensor')
def sensor():
	return render_template('sensor.html')'''

@app.route('/graphs')
def graphs():
	db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
	cur = db.cursor()
	h=[]
	k=[]
	u=[]
	d=[]
	count=0
	count1=0
	cur.execute("SELECT Temperature FROM Weather")
	for row in cur.fetchall():
		h.append(row)
		count=count+1
	cur.execute("SELECT Humidity FROM Weather")
	for row in cur.fetchall():
		u.append(row)
		count1=count1+1
	#print type(h)
	#print h
	k=list(chain(*h))
	d=list(chain(*u))
	x=[]
	#print k
	j=[]
	for i in range(count-7,count):
		o=float(k[i])
		j.append(o)
	for i in range(count-7,count):
		o=float(d[i])
		x.append(o)
	return render_template('graphs.html',j=j,x=x,k=k)



@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email  = request.form['username']
		password  = request.form['password']
		phno      = request.form['phno']
		place      = request.form['place']
		print email
		print password
		print phno
		print place
		db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
		cur = db.cursor()
		cur.execute("SELECT COUNT(1) FROM Users WHERE email = %s;", [email])
		k=cur.fetchone()[0]
		if k==0:
			cur.execute('''INSERT INTO Users(email,password,phno,place) values(%s, %s, %s, %s)''',(email,password,phno,place))
			db.commit()
			cur.close()
			return redirect(url_for('signin'))
		else:
			error="User Already Exists"
			print error
			return render_template('signup.html',error=error)		
	return render_template('signup.html')	




@app.route('/signin',methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email  = request.form['email']
		password  = request.form['password']
		db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
		cur = db.cursor()
		cur.execute("SELECT COUNT(1) FROM Users WHERE email = %s;", [email])
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM Users WHERE email = %s;", [email])
			for row in cur.fetchall():
				if password==row[0]:
					cur.execute("SELECT phno FROM Users WHERE email = %s;", [email])
					phno=cur.fetchone()[0]
					cur.execute("SELECT place FROM Users WHERE email = %s;", [email])
					place=cur.fetchone()[0]
					cur.close()
					session['email']=email
					session['phno']=phno
					session['place']=place
					return redirect(url_for('profile'))
				else:
					return redirect(url_for('signin'))
		else:
			return redirect(url_for('signin'))
	return render_template('signin.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')




@app.route('/profile')
def profile():
	email=session['email']
	place=session['place']
	g=geocoder.google(place)
	lat1=str(g.lat)
	lon1=str(g.lng)
	url="http://api.openweathermap.org/data/2.5/weather?lat="+lat1+"&lon="+lon1+"&APPID=1b7843ebea1f3c96215fb1a374e6e1b6"
	
	place1=session['place']
	phno=session['phno']
	
	
	res2 = urllib2.urlopen(url)
	b= res2.read()
	b1 = b.replace("'", "\"")
	html2= json.loads(b1)	
	humidity=str(html2['main']['humidity'])
	temperature2=float(html2['main']['temp'])-273
	temperature=str(temperature2)
	speed2=float(html2['wind']['speed'])*1.609
	speed=str(speed2)
	pressure=str(float(html2['main']['pressure'])*0.0009)
	direc=str(html2['wind']['deg'])
	weather=html2['weather'][0]['main']
	
	me = "noreplyweathersricity@gmail.com"
	you = session['email']
    #print me
    #print you
	print "email"
	text= "place:"+session['place']+"\nWeather:"+weather+"\nTemperature : "+temperature+" degrees celsius\n Humidity : "+humidity+"%\nPressure :"+pressure+"atm\nWind speed :"+speed+"kmph\nWind Direction :"+direc+" degree\n"
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Weather alert!"
	msg['From'] = me
	msg['To'] = you
	part1 = MIMEText(text, 'plain')
	msg.attach(part1)
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login('noreplyweathersricity', 'iiits@123')
	mail.sendmail(me, you, msg.as_string())
	mail.quit()
	
	
	"""username = "9505768468"
	passwd = "sucharita"
	number=session['phno']
	message="Weather:"+weather+"\nTemperature : "+temperature+" degrees celsius\n Humidity : "+humidity+"%\nPressure :"+pressure+"atm\nWind speed :"+speed+"kmph\nWind Direction :"+direc+" degree\n"
	message = "+".join(message.split(' '))
	print "sms"
	#logging into the sms site
	url ='http://site24.way2sms.com/Login1.action?'
	data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
	#For cookies
	cj= cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	#Adding header details
	opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
	try:
		usock =opener.open(url, data)
	except IOError:
		print "error"
	jession_id =str(cj).split('~')[1].split(' ')[0]
	send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
	send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
	opener.addheaders=[('Referer', 'http://site24.way2sms.com/sendSMS?Token='+jession_id)]
	try:
		sms_sent_page = opener.open(send_sms_url,send_sms_data)
	except IOError:
		print "error"
	print "success"
	"""
	x=datetime.datetime.now()
	now=str(x)
	account_sid = "AC84d1ee03673d8ac123bb48352660a4fc"
	auth_token = "e9551ad9e86a0eaf9b64ac99b4d97d4d"
	client = TwilioRestClient(account_sid, auth_token)
	s="User:"+email+" logged in and placed a query for "+place+" at "+now+"\n"
	message = client.messages.create(to="+918096311688", from_="+1 201-720-4741 ",
                                     body=s)
	#print "success"
	print "success sms sent"
	
	return render_template('profile.html',email=email,humidity=humidity,temperature=temperature2,pressure=pressure,speed=speed,direc=direc,weather=weather,place=place,phno=phno)



@app.route('/Psettings', methods= ['GET', 'POST'])
def Psettings():
	if request.method == 'POST':
		email=session['email']
		place=session['place']
		uplace=request.form['uplace']
		db = MySQLdb.connect(host="localhost", user="root", passwd="Sur 0810", db="Weather")
		cur = db.cursor()
		query = """ UPDATE Users SET place = %s WHERE email = %s """
		data = (uplace,email)
		cur.execute(query,data)
		db.commit()
		cur.close()
		print "super"
		session['place']=uplace
		return redirect(url_for('profile'))
	return render_template('Psettings.html',email=session['email'],place=session['place'])
	
	
@app.route('/latlon', methods=['GET', 'POST'])
def latlon():
    if request.method == 'POST':
        place=request.form['place']
        return redirect(url_for('index'))
    return redirect(url_for('index'))





@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('phno', None)
    session.pop('place', None)
    return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=True)
