import requests
import base64
import os
import urllib.parse

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
    
    def get_user_profile(self, access_token):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        response.raise_for_status()  # raise exception if response is not 200
        return response.json()



    # class UserData(SpotifyClient):
    #     def __init__(self, client_id, client_secret, redirect_uri, access_token) -> None:
    #         super().__init__(client_id, client_secret, redirect_uri)
    #         self.access_token = access_token

