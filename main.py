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

@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Redirect to Spotify's login page
    """
    authorization_url = spotify_client.request_auth_url()
    return redirect(authorization_url)

@app.route("/callback", methods=['GET'])
def callback():
    """
    Handle callback from Spotify after user login
    """
    # Extract authorization code from query parameters
    authorization_code = request.args.get('code')
    state = request.args.get('state')

    # Exchange authorization code for access token
    access_token_info = spotify_client.exchange_code_for_token(authorization_code, state)
    
    # Store access token in session
    session['access_token'] = access_token_info['access_token']
    return redirect(url_for('home'))

@app.route("/home", methods=['GET'])
def home():
    """
    Render home page after successful login
    """
    return render_template('index.html')

#-------------------------------- RECOMMENDATIONS ---------------------------------
# Artist recommendations

# Song recommendations

#--------------------------------- ERROR HANDLER ---------------------------------


#--------------------------------- RUN LOCALLY --------------------------------- 
if __name__ == '__main__':
    app.run(debug=True, port=5500)