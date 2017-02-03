from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
#use SQLAlchemy to link with postgres DB
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ee:123@localhost/mydb'  #set up the link
app.config['SECRET_KEY']=os.urandom(4)
app.config['DEBUG']=False

db=SQLAlchemy(app)

class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(10),unique=True)
	email=db.Column(db.String(20),unique=False)

	def __init__(self, username, email):
		self.username=username
		self.email=email

	def __repr__(self):
		return '<User {}>'.format(self.username)

# REFRESH homepage to show UI and data   (view)
@app.route('/')
def index():
	# get all items in table 'user'
	dblist=User.query.all()
	return render_template("home.html",dblist=dblist)

# ADD new user info to the database   (processing)
@app.route('/add',methods=['POST'])
def add():	
	username=request.form['username']
	email=request.form['email']
	if username and email: # add entry to db only when username and email from html are both not empty
		user=User(username,email) # add data in object user to table 'user'
		db.session.add(user)
		db.session.commit()
		flash("new user entry was added")
	return redirect(url_for('index'))

# SEARCH data record by username   (processing)
@app.route('/search', methods=['POST'])
def search ():	
	searchdb=[]	
	searchdb=User.query.filter_by(username=request.form['searchkw'])
	return render_template('search.html',searchdb=searchdb)
	

if __name__=="__main__":
	app.run(debug=True)
