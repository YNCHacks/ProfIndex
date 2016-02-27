# -*- coding: utf-8 -*-

from app import app
from app.controllers.controller import *
from flask import render_template, request, g, session

app.secret_key = '\x90\xfd*"\x9e\'\xe2]\xbd\xa3\x8f,\xca\\\x0e\xd9\x92\xdd\xdc~\xcfKM\x8d'

"""
    The views file.
    This is where all the view functions go

    Make sure to add docstrings!
"""

controller = Controller()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def render_login_page():
    return render_template('login.html')

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
    prof = controller.search_prof(prof_name)
    if (prof.availability == True):
        status = "Is in office "
    else:
        status = "Is not in "
    return render_template('prof.html', prof=prof.name, status=status + prof.office, image=prof.picture_url)

@app.route('/update_prof_availability/<email>', methods=['POST'])
def update_prof_availability(email):
    prof_availability = request.form.get('avail', None)
    if (prof_availability == "on"):
        prof_availability = True
    else:
        prof_availability = False
    controller.update_value(email, 'availability', prof_availability)
    if ('username' in session):
        prof_object = controller.search_prof(session['username'])
        return render_template('account.html', result=prof_object)
    return render_template('index.html')
