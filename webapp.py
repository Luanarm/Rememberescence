from flask import Flask, render_template, request, jsonify
import cohere
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#cohere_api_key = os.getenv("CO_API_KEY")
cohere_api_key = "s5yafntwVwUN7J108V11n9y4YceYj9ZvjAzBMAjI"
print(f"API Key: {cohere_api_key}")
co = cohere.Client(cohere_api_key)

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id='55be60be52eb4b658763757653391641', 
                                                      client_secret='8ce1ad629229430ab7d2d7278ebdb9bd')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.json

    # Get user inputs from the JSON data
    user_interests = data.get("interests")
    user_location = data.get("location")
    user_age = data.get("age")
    user_friends = data.get("friends")

    print(user_friends)

    # Use Cohere to generate content based on user inputs
    parameters = f'Friends:{user_friends}, Interests: {user_interests}, Location: {user_location}'
    generation_response = co.generate(
        prompt=f'Please write a short story for nostalgia based on these parameters: {parameters} addressing the user as "you"'
    )

    # User's age & location used for childhood Spotify


    # Access the 'text' attribute to get the generated content
    generated_content = generation_response[0].text

    # Return the JSON response with the generated content
    return jsonify({"generated_content": generated_content})

if __name__ == '__main__':
    app.run(debug=True)