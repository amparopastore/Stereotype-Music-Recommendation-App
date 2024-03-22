import requests
import base64

class SpotifyClient:
    AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize?'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    #STATE = ''
    SCOPE = 'user-top-read playlist-read-private'

    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None

    def request_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            #'state': self.STATE,
            'scope': self.SCOPE
        }
        return requests.Request('GET', self.AUTHORIZATION_URL, params=params).prepare().url
    
    def exchange_code_for_token(self, code):
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
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return response.json()
        else:
            # raise exception with error message
            response.raise_for_status()
    
    def get_user_profile(self, access_token):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        response.raise_for_status()  # raise exception if response is not 200
        return response.json()



    # class UserData(SpotifyClient):
    #     def __init__(self, client_id, client_secret, redirect_uri, access_token) -> None:
    #         super().__init__(client_id, client_secret, redirect_uri)
    #         self.access_token = access_token

