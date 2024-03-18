#--------------------------------- IMPORTS ---------------------------------
import flask
from flask import Flask, render_template, redirect, url_for, session, request
import os


# initialize flask app instance
app = Flask(__name__)

# configuration settings
app.secret_key = os.random(2)
app.config['SESSION_COOKIE_NAME'] = "AppName Cookie"
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


#--------------------------------- LOGIN/HOME ---------------------------------

@app.route("/", methods=['GET'])
def index():
    """
    Redirect users to login page
    """

@app.route("/login", methods=['GET'])
def login():
    """
    Redirect to Spotify's login page
    """

@app.route("/callback", methods=['GET'])
def callback():
    """
    Handle callback from Spotify after user login
    """

@app.route("/home", methods=['GET'])
def home():
    """
    Render home page after successful login
    """

#-------------------------------- RECOMMENDATIONS ---------------------------------
# Artist recommendations

# Song recommendations

#-------------------------------- DASHBOARD ---------------------------------

#--------------------------------- ERROR HANDLER ---------------------------------