# -*- coding: utf-8 -*-

from app import app
from app.controllers.controller import *
from flask import render_template, request, g, session, redirect, url_for
from flask.ext.login import LoginManager, login_required
from functools import wraps
import urllib2, re

app.secret_key = '\x90\xfd*"\x9e\'\xe2]\xbd\xa3\x8f,\xca\\\x0e\xd9\x92\xdd\xdc~\xcfKM\x8d'

"""
    The views file.
    This is where all the view functions go

    Make sure to add docstrings!
"""

controller = Controller()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'render_login_page'

def get_image_url(fname, lname):
    url = "https://www.yale-nus.edu.sg/about/faculty/" + fname + "-" + lname
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    try:
        page = urllib2.urlopen(req)
        html = page.read()
        matches = re.findall('src="([^"]+)"', html)[7]
    except:
        matches = "http://www.allegraabbotsford.com/wp-content/uploads/2015/06/generic-profile.png"
    return matches

@app.route('/')
def index():
    names = controller.get_all_professor_names()
    return render_template('index.html', names=names)

@app.route('/signup/')
def render_signup_page():
    return render_template('signup.html')

@app.route('/login/')
def render_login_page():
    names = controller.get_all_professor_names()
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/new_user/', methods=['POST'])
def create_new_user():
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    name = fname + " " + lname
    location = request.form['location']
    hours = request.form['hours']
    img_url = get_image_url(fname, lname)
    prof_properties = {"name": name, "email": email, "password": password, "office": location, "office_hours": hours, "availability": False, "picture_url": img_url, 'id': 'id'}
    controller.add_professor(prof_properties)
    
    result = controller.authenticate(email, password)
    if (result[0]):
        session['username'] = result[1].name
        return render_template('account.html', result=result[1])
    return render_login_page() #change to error page

@app.route('/create_account/')
def render_create_account_page():
    return render_template('create_account.html')

@app.route('/prof/<uuid>')
def render_permalinked_prof_page(uuid):
    prof = controller.search_prof(uuid, 'id')
    if (prof.availability == True):
        status = "Is in office "
    else:
        status = "Is not in "
    return render_template('prof.html', prof=prof.name, status=status + prof.office, image=prof.picture_url)

@app.route('/validate_login_information/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    result = controller.authenticate(email, password)
    if (result[0]):
        session['username'] = result[1].name
        return render_template('account.html', result=result[1])
    return render_login_page()

@app.route('/search_prof/', methods=['POST'])
def render_prof_page():
    prof_name = request.form['prof_name']
    result = controller.search_prof(prof_name)
    if (result[0]):
        prof = result[1]
        if (prof.availability == True):
            status = "Is in office "
        else:
            status = "Is not in "
        return render_template('prof.html', prof=prof.name, status=status + prof.office, image=prof.picture_url)
    return index()

@app.route('/update_prof_availability/')
@login_required
def update_prof_availability():
    prof_email = request.args.get('prof_email', '1', type=str)
    prof_availability = request.args.get('state', '1', type=str)
    if (prof_availability == "true"):
        prof_availability = True
    else:
        prof_availability = False
    controller.update_value(prof_email, 'availability', prof_availability)
    prof_object = controller.search_prof(session['username'])
    return render_template('account.html', result=prof_object)
