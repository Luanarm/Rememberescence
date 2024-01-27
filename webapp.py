from flask import Flask, render_template, request, jsonify
import cohere
import requests
from base64 import b64encode

app = Flask(__name__)

# Initialize Cohere client
cohere_api_key = "s5yafntwVwUN7J108V11n9y4YceYj9ZvjAzBMAjI"
co = cohere.Client(cohere_api_key)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.json

    # Get user inputs from the form data
    user_interests = data.get("interests")
    user_location = data.get("location")
    user_age = data.get("age")
    user_genre = data.get("genre")

    # Use Cohere to generate content based on user inputs
    generation_response = co.generate(
        prompt=f'Please write a short story for nostalgia based on these parameters: {user_interests} {user_location}'
    )

    # Access the 'text' attribute to get the generated content
    generated_content = generation_response[0].text

    # Obtain Spotify access token
    access_token = get_spotify_access_token()

    if access_token:
        playlist_generated = generate_playlist(access_token, user_location, user_age, user_genre)
        if playlist_generated:
            return jsonify({"generated_content": generated_content, "playlist_created": True})
        else:
            return jsonify({"generated_content": generated_content, "playlist_created": False})
    else:
        return jsonify({"generated_content": generated_content, "playlist_created": False, "error": "Failed to get Spotify access token."})

def get_spotify_access_token():
    SPOTIFY_CLIENT_ID = "0c29685d3fcb4c2b8f9903cf7238f15a"
    SPOTIFY_CLIENT_SECRET = "7710bfaff25748eaa626f5facfd2d89b"
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"

    # Request access token from Spotify API
    auth_response = requests.post(
        SPOTIFY_AUTH_URL,
        headers={"Authorization": "Basic " + b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()},
        data={"grant_type": "client_credentials"}
    )

    if auth_response.status_code == 200:
        auth_response_data = auth_response.json()
        access_token  = auth_response_data.get("access_token")
        return access_token
    else:
        return None
    
    

def generate_playlist(access_token, location, age, genre):
    tracks = search_tracks(access_token, location, age, genre)

    if not tracks:
        return False
    
    playlist_id = create_playlist(access_token)
    
    if not playlist_id:
        return False  # Playlist creation failed

    # Step 3: Add tracks to the playlist
    if not add_tracks_to_playlist(access_token, playlist_id, tracks):
        return False  # Failed to add tracks to the playlist

    return True  # Playlist generated successfully

def search_tracks(access_token, location, age, genre):
    # Construct the query string for searching tracks
    query = f"genre:{genre} year:{age} country:{location}"
    
    # Make a request to the Spotify API's search endpoint
    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"q": query, "type": "track", "limit": 10}  # Adjust limit as needed
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response to extract track URIs
        tracks = response.json().get("tracks", {}).get("items", [])
        track_uris = [track["uri"] for track in tracks]
        return track_uris
    else:
        return None  # Failed to search tracks
    
def create_playlist(access_token):
# Define the playlist name
    playlist_name = "Your Personalized Playlist"
    
    # Make a request to the Spotify API's endpoint to create a playlist
    response = requests.post(
        "https://api.spotify.com/v1/me/playlists",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"name": playlist_name, "public": False}  # Adjust public/private as needed
    )
    
    # Check if the request was successful
    if response.status_code == 201:
        # Parse the response to obtain the playlist ID
        playlist_id = response.json().get("id")
        return playlist_id
    else:
        return None  # Failed to create playlist
    
def add_tracks_to_playlist(access_token, playlist_id, tracks):
    # Make a request to the Spotify API's endpoint to add tracks to the playlist
    response = requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"uris": tracks}
    )
    
    # Check if the request was successful
    if response.status_code == 201:
        return True  # Tracks added successfully
    else:
        return False  # Failed to add tracks to the playlist

if __name__ == '__main__':
    app.run(debug=True)
