
import os
from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Use a more persistent session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

@app.route('/')
def index():
    sp_oauth = SpotifyOAuth(
    ,
        ,
        redirect_uri="http://127.0.0.1:5000/callback",
        scope="",
    )
    auth_url = sp_oauth.get_authorize_url()
    return f'<a href="{auth_url}">Authorize with Spotify</a>'

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
      ,
       ,
        redirect_uri="http://127.0.0.1:5000/callback",
        scope="",
    )

