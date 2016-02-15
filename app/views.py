# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request

"""
    The views file.
    This is where all the view functions go

    Make sure to add docstrings!
"""

@app.route('/')
def index():
    return render_template('index.html', name="Ross")

@app.route('/login/')
def render_login_page():
    return render_template('login.html')



@app.route('/validate_login_information/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return render_template('account.html', username=username, password=password, image="https://www.yale-nus.edu.sg/wp-content/uploads/2015/07/stanislav-presolski-headshot-380x507.jpg")

@app.route('/search_prof/', methods=['POST'])
def render_prof_page():
    prof_name = request.form['prof_name']
    office = "RC1-asdf"
    return render_template('prof.html', prof=prof_name, status="Is in office " + office, image="https://www.yale-nus.edu.sg/wp-content/uploads/2015/07/stanislav-presolski-headshot-380x507.jpg")
