import requests
import base64
import os
import urllib.parse
import random

from collections import Counter

class SpotifyClient:
    AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    
    #STATE = ''
    SCOPE = 'user-top-read playlist-read-private'
    SHOW_DIALOG = True

    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.state = None

    def gen_rand_str(self, length):
        return os.urandom(length).hex()
    
    #  ------------------ Authorization ------------------
    def request_auth_url(self):
        self.state = self.gen_rand_str(16)
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': self.SCOPE,
            'show_dialog': str(self.SHOW_DIALOG).lower(),
            'state': self.state
        }
        # return requests.Request('GET', self.AUTHORIZATION_URL, params=params).prepare().url
        return f"{self.AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    
    def exchange_code_for_token(self, code, state):
        if state != self.state:
            raise ValueError("State mismatch")
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        token_info = response.json()
        self.access_token = token_info['access_token']
        return token_info

    def get_user_profile(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        response.raise_for_status()  # raise exception if response is not 200
        return response.json()

# ------------------ Recommendations ------------------
    
    def get_top_items(self, type='artists'):
        url = f'https://api.spotify.com/v1/me/top/{type}'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(url, headers=headers)
        return response.json()['items']

    
    def get_artist_recommendations(self):
        endpoint_url = 'https://api.spotify.com/v1/artists/{id}/related-artists'
        top_artists = self.get_top_items(type='artists') 
        seed_artists = [artist['id'] for artist in top_artists[:5]] 
        headers = {'Authorization': f'Bearer {self.access_token}'}
        recommendations = []
        for artist_id in seed_artists:
            url = endpoint_url.format(id=artist_id)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                related_artists_data = response.json().get('artists', [])
                if related_artists_data:  # check if there are related artists
                    selected_related_artist = random.choice(related_artists_data)
                    artist_info = {
                        'id': selected_related_artist['id'],
                        'name': selected_related_artist['name'],
                        'external_urls': selected_related_artist['external_urls']['spotify'],
                        'popularity': selected_related_artist['popularity'],
                        'followers': selected_related_artist['followers'],  # fetching followers
                        'images': selected_related_artist['images']  # fetching images
                    }
                    recommendations.append(artist_info)
            else:
                print(f"Failed to fetch related artists for artist with ID {artist_id}")
        return recommendations


    def get_track_recommendations(self):
        endpoint_url = 'https://api.spotify.com/v1/recommendations'
        top_tracks = self.get_top_items(type='tracks')  
        seed_tracks = [track['id'] for track in top_tracks[:5]]
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'seed_tracks': ','.join(seed_tracks)}
        response = requests.get(endpoint_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
