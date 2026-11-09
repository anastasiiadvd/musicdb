#import functions from flask
from flask import render_template, flash, redirect, url_for, session

#import the package to connect to postgreSQL and the functions to hash and check passwords
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

#import app variable from app package
from app import app

#import the forms
from app.forms import LoginForm, RegistrationForm


def get_db_connection():
    #connect to the database using the settings in config.py
    return psycopg2.connect(database=app.config['DB_NAME'], user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'], host=app.config['DB_HOST'],
                            port=app.config['DB_PORT'])


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


#create an association for the URL /register, GET shows the form and POST receives it
@app.route('/register', methods=['GET', 'POST'])
def register():
    #a user who is already logged in does not need to register
    if 'username' in session:
        return redirect(url_for('index'))

    form = RegistrationForm()

    #this is true when the form was submitted and every validator passed
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()

        conn = get_db_connection()
        cur = conn.cursor()

        #check that the username and the email are not already used
        #(%s is used instead of joining strings because the text was typed by a user)
        cur.execute("select user_id from users where username = %s or email = %s", (username, email))
        existing = cur.fetchone()

        if existing is not None:
            cur.close()
            conn.close()
            flash('That username or email is already registered.')
            return render_template('register.html', title='Register', form=form)

        #insert the new user, the password is hashed first
        cur.execute("insert into users (username, email, password_hash) values (%s, %s, %s)",
                    (username, email, generate_password_hash(form.password.data)))

        #commit the sql code to the database and close the connection
        conn.commit()
        cur.close()
        conn.close()

        flash('Account created. Please sign in.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


#create an association for the URL /login, GET shows the form and POST receives it
@app.route('/login', methods=['GET', 'POST'])
def login():
    #a user who is already logged in does not need to log in again
    if 'username' in session:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()

        conn = get_db_connection()
        cur = conn.cursor()

        #find the user, then close the connection
        cur.execute("select user_id, password_hash, role from users where username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        #hash the password that was typed and compare it with the hashed password in the table
        if user is None or not check_password_hash(user[1], form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        #remember who is logged in
        session['user_id'] = user[0]
        session['username'] = username
        session['role'] = user[2]

        #if Remember Me was ticked the login lasts after the browser is closed
        session.permanent = bool(form.remember_me.data)

        flash('Welcome back, ' + username + '!')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


#create an association for the URL /logout
@app.route('/logout')
def logout():
    #forget who was logged in
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))
