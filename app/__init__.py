# -*- coding: utf-8 -*-

"""
Initialization of the app (In general don't need to touch)
"""

from flask import Flask

app = Flask(__name__)

# This is the last line to avoid any import errors
from app import views
