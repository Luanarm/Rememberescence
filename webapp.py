from flask import Flask, render_template, request, jsonify
import cohere
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)

#cohere_api_key = os.getenv("CO_API_KEY")
cohere_api_key = "s5yafntwVwUN7J108V11n9y4YceYj9ZvjAzBMAjI"
print(f"API Key: {cohere_api_key}")
co = cohere.Client(cohere_api_key)

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id='55be60be52eb4b658763757653391641', 
                                                      client_secret='8ce1ad629229430ab7d2d7278ebdb9bd')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    if session.get('user'):
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        return render_template("login.html")

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
        prompt=f'Please write a nostalgic short story about the users childhood based on these parameters: {parameters} addressing the user as "you"'
    )

    # User's age & location used for childhood Spotify


    # Access the 'text' attribute to get the generated content
    generated_content = generation_response[0].text

    # Return the JSON response with the generated content
    return jsonify({"generated_content": generated_content})

if __name__ == '__main__':
    app.run(debug=True)