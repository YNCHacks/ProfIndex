# -*- coding: utf-8 -*-

from app import app
from app.controllers.controller import *
from flask import render_template, request, g, session

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
    if (result != "Failed Login. Please check your entered credentials."):
        return render_template('account.html', result)

@app.route('/search_prof/', methods=['POST'])
def render_prof_page():
    prof_name = request.form['prof_name']
    prof = controller.search_prof(prof_name)
    if (prof.availability == True):
        status = "Is in office "
    else:
        status = "Is not in "
    return render_template('prof.html', prof=prof.name, status=status + prof.office, image=prof.picture_url)
