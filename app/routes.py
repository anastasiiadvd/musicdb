#import render_template function from flask
from flask import render_template

#import app variable from app package
from app import app


#create an association for the URL /
@app.route('/')
#create an association for the URL /index
@app.route('/index')
def index():
    #create the home page
    return render_template('index.html', title='Music Discovery Database')


#create an association for the URL /about
@app.route('/about')
def about():
    #create the about us page
    return render_template('about.html', title='About Us')
