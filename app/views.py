# -*- coding: utf-8 -*-

"""
    The views file.
    This is where all the view functions go
"""

from app import app
from flask import render_template, redirect, url_for, request

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
