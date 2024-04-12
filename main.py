#--------------------------------- IMPORTS ---------------------------------
import flask
from flask import Flask, render_template, redirect, url_for, session, request
import os
from helpers.client import SpotifyClient
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


#--------------------------------- LOGIN/HOME PAGE ---------------------------------
spotify_client = SpotifyClient(client_id, client_secret, redirect_uri)

@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Redirect to Spotify's login page
    """
    authorization_url = spotify_client.request_auth_url()
    return render_template('index.html', authorization_url=authorization_url)

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
    user_profile = spotify_client.get_user_profile()
    return render_template('index.html', user_profile=user_profile)

@app.route("/about",  methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/trending",  methods=['GET'])
def trending():
    return render_template('trending.html')

#-------------------------------- RECOMMENDATIONS PAGE ---------------------------------
# Artist & track recommendations

@app.route("/recommend_start", methods=['GET', 'POST'])
def recommend_start():
    if request.method == 'GET':
        return render_template('recommend_start.html')
    elif request.method == 'POST':
        seed_type = request.form['seed_type'] 
        if seed_type == 'artist':
            return redirect(url_for('recommend_artists'))
        elif seed_type == 'track':
            return redirect(url_for('recommend_songs'))

@app.route("/recommend_artists", methods=['GET', 'POST'])
def recommend_artists():
    top_artists = spotify_client.get_top_items(type='artists')
    recommendations = spotify_client.get_artist_recommendations()
    return(render_template('artists_recs.html', top_artists=top_artists, recommendations=recommendations))

@app.route("/recommend_songs", methods=['GET', 'POST'])
def recommend_songs():
    top_songs = spotify_client.get_top_items(type='tracks')
    recommendations = spotify_client.get_track_recommendations()
    return(render_template('songs_recs.html', top_songs=top_songs, recommendations=recommendations))


#--------------------------------- ERROR HANDLER ---------------------------------


#--------------------------------- RUN LOCALLY --------------------------------- 
if __name__ == '__main__':
    app.run(debug=True, port=5500)