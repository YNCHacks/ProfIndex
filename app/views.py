# -*- coding: utf-8 -*-

from app import app
from app.controllers.controller import *
from flask import render_template, request, g, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
#from boto3.s3.connection import S3Connection
import urllib2, re, flask, uuid

app.secret_key = '\x90\xfd*"\x9e\'\xe2]\xbd\xa3\x8f,\xca\\\x0e\xd9\x92\xdd\xdc~\xcfKM\x8d'

"""
    The views file.
    This is where all the view functions go
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

"""
    Required for using login_manager.
    Returns Professor class
"""
@login_manager.user_loader
def load_user(username):
    return controller.search_prof(username)[1]

"""
    Renders the home page
    Requires a list of all professor names for autocomplete
"""
@app.route('/')
def index():
    names = controller.get_all_professor_names()
    return render_template('index.html', names=names, current_user=current_user)

"""
    Renders the login page
"""
@app.route('/login/')
def render_login_page():
    return render_template('login.html')


"""
    Validates form information from the login page rendered above.
    Uses login_manager to log the user in
    Redirects the user to account page
"""
@app.route('/validate_login_information/', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    result = controller.authenticate(email, password)
    if (result[0]):
        login_user(result[1], remember=True)
        return flask.redirect(flask.url_for('render_account_page'))
    return flask.render_template('login.html') #TODO: Errors

"""
    When a user is logged in,
    Renders the account page based on the current logged in user.
"""
@app.route('/account/')
@login_required
def render_account_page():
    return render_template('account.html') #TODO: change result to current_user in html.

"""
    When a user is logged in,
    Uses login_manager to log out a user,
    Redirects user to home page.
"""
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))

"""
    Renders the signup page
"""
@app.route('/signup/')
def render_signup_page():
    return render_template('signup.html')

"""
    Pulls form information from the form on the create account page (rendered above)
    Gets an image from the Yale-NUS website for professors.
    Makes a dictionary with the information,
    adds professor with Dictionary

    Logs in new user,
    renders account page.
"""
@app.route('/new_user/', methods=['POST'])
def create_new_user():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    prof_properties = {"name": fname + " " + lname,
                        "email": email,
                        "password": password,
                        "office": request.form['location'],
                        "office_hours": request.form['hours'],
                        "availability": False,
                        "picture_url": get_image_url(fname, lname),
                        'id': str(uuid.uuid4())}

    controller.add_professor(prof_properties)

    result = controller.authenticate(email, password)
    if (result[0]):
        user = result[1]
        login_user(user, remember=True)
        return flask.redirect(flask.url_for('render_account_page'))
    return render_login_page() #TODO: change to error page

"""
    Renders a professor's page based on uuid
"""
@app.route('/prof/<uuid>')
def render_permalinked_prof_page(uuid):
    prof = controller.search_prof(uuid, 'id')
    if (prof.availability == True):
        status = "Is in office "
    else:
        status = "Is not in "
    return render_template('prof.html', prof=prof, status=status + prof.office) #TODO: do this in HTML instead

"""
    Gets prof name from search bar,
    Matching prof object returned from controller
    Renders prof page
"""
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
        return render_template('prof.html', prof=prof, status=status + prof.office)
    return index() #TODO: Errors

"""
    Retrieves JSON data from prof's account page
    Updates prof's status on the server
"""
@app.route('/update_prof_availability/')
def update_prof_availability():
    prof_availability = request.args.get('state', '1', type=str)
    print(prof_availability)
    if (prof_availability == "true"):
        prof_availability = True
    else:
        prof_availability = False
    print(current_user.email)
    controller.update_value(current_user.email, 'availability', prof_availability)
    return render_template('account.html')
