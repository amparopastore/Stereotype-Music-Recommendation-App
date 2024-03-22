#--------------------------------- IMPORTS ---------------------------------
import flask
from flask import Flask, render_template, redirect, url_for, session, request
import os
from user import SpotifyClient
import config

# initialize flask app instance
app = Flask(__name__)

# configuration settings
app.secret_key = os.urandom(2)
app.config['SESSION_COOKIE_NAME'] = "StereoType Cookie"
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
client_id = config.SPOTIFY_CLIENT_ID
client_secret = config.SPOTIFY_CLIENT_SECRET
redirect_uri = config.REDIRECT_URI


#--------------------------------- LOGIN/HOME ---------------------------------
spotify_client = SpotifyClient(client_id, client_secret, redirect_uri)

@app.route("/", methods=['POST', 'GET'])
def index():
    """
    Redirect to Spotify's login page
    """
    authorization_url = spotify_client.request_authorization_url()
    return redirect(authorization_url)

@app.route("/callback/q")
def callback():
    """
    Handle callback from Spotify after user login
    """
    # Extract authorization code from query parameters
    authorization_code = request.args['code']
    
    # Exchange authorization code for access token
    access_token_info = spotify_client.exchange_code_for_token(authorization_code)

    # Store access token in session
    if access_token_info:
        session['access_token'] = access_token_info['access_token']
        return redirect(url_for('home',_external=True))
    
    return "Authentication failed."

@app.route("/home")
def home():
    """
    Render home page after successful login
    """
    if 'access_token' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('index'))

#-------------------------------- RECOMMENDATIONS ---------------------------------
# Artist recommendations

# Song recommendations

#--------------------------------- ERROR HANDLER ---------------------------------


#--------------------------------- RUN LOCALLY --------------------------------- 
if __name__ == '__main__':
    app.run(debug=True, port=5500)