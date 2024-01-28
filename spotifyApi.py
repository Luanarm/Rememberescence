# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     sp_oauth = SpotifyOAuth(
#        "0c29685d3fcb4c2b8f9903cf7238f15a",
#         "7710bfaff25748eaa626f5facfd2d89b",
#         redirect_uri="http://127.0.0.1:5000/",
#         scope="",
#     )
#     auth_url = sp_oauth.get_authorize_url()
#     return f'<a href="{auth_url}">Authorize with Spotify</a>'

# @app.route('/callback')
# def callback():
#     sp_oauth = SpotifyOAuth(
#         "0c29685d3fcb4c2b8f9903cf7238f15a",
#         "7710bfaff25748eaa626f5facfd2d89b",
#         redirect_uri="http://127.0.0.1:5000/",
#         scope="",
#     )
#     token_info = sp_oauth.get_access_token(request.args['code'])
#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     playlists = sp.current_user_playlists()
#     return str(playlists)

# if __name__ == '__main__':
#     app.run(debug=True, port=8888)
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
        "0c29685d3fcb4c2b8f9903cf7238f15a",
        "7710bfaff25748eaa626f5facfd2d89b",
        redirect_uri="http://127.0.0.1:5000/callback",
        scope="",
    )
    auth_url = sp_oauth.get_authorize_url()
    return f'<a href="{auth_url}">Authorize with Spotify</a>'

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        "0c29685d3fcb4c2b8f9903cf7238f15a",
        "7710bfaff25748eaa626f5facfd2d89b",
        redirect_uri="http://127.0.0.1:5000/callback",
        scope="",
    )

#     # Get user input
#     user_interests = request.args.get("interests")
#     user_location = request.args.get("location")
#     user_age = request.args.get("age")
#     print(user_age)
#     user_genre = request.args.get("genre")

#     token_info = sp_oauth.get_access_token(request.args['code'])
#     sp = spotipy.Spotify(auth=token_info['access_token'])

#     # Your logic to calculate the year based on user's age
#     current_year = 2024  # Replace with the current year
#     birth_year = current_year - int(user_age)

#     # Your logic to create a playlist name based on user input
#     playlist_name = f"{user_interests} Playlist {birth_year} {user_location}"

#     # Your logic to find or create a playlist
#     playlists = sp.current_user_playlists()
#     playlist_exists = False
#     playlist_id = None

#     for playlist in playlists['items']:
#         if playlist['name'] == playlist_name:
#             playlist_exists = True
#             playlist_id = playlist['id']
#             break

#     if not playlist_exists:
#         # Create a new playlist
#         playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name)
#         playlist_id = playlist['id']

#     return redirect(url_for('show_playlist', playlist_id=playlist_id))

# @app.route('/show_playlist/<playlist_id>')
# def show_playlist(playlist_id):
#     return f'Playlist ID: {playlist_id}'

if __name__ == '__main__':
    app.run(debug=True, port=8888)
