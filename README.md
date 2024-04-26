# StereoType Flask App

StereoType is a Flask web application that provides Spotify recommendations based on user's top artists and tracks.

## Features

- Spotify login using OAuth 2.0
- View user profile information
- View top artists and tracks
- Get artist recommendations
- Get song recommendations

## Prerequisites

Before running this application, you need to have:

- Python 3.x installed
- Spotify Developer account to get `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`
- A `.env` file in the project root directory with the following environment variables:

    ```
    SPOTIFY_CLIENT_ID=your_client_id
    SPOTIFY_CLIENT_SECRET=your_client_secret
    REDIRECT_URI=your_redirect_uri
    ```

- If running locally on port 5500, for instance, the redirect uri will be 'http://127.0.0.1:5500/callback'

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/amparopastore/Stereotype-Music-Recommendation-App
    ```

2. Navigate to the project directory:

    ```bash
    cd stereotype-flask-app
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

To run the app locally, execute:

```bash
python app.py
