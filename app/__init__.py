# -*- coding: utf-8 -*-

"""
Initialization of the app
"""

from flask import Flask

app = Flask(__name__)

# This is the last line to avoid any import errors
from app import views, models
