# -*- coding: utf-8 -*-

"""
    The views file.
    This is where all the view functions go
"""

from app import app
from app.controllers.controller import get_name
from flask import render_template, redirect, url_for, request

@app.route("/")
def index():
    name = get_name()
    return render_template("index.html", name=name)

@app.route("/hello")
def hello():
    return render_template("hello.html", food="sushi")
