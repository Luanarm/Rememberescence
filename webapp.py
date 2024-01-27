from flask import Flask, render_template, request, jsonify
import cohere
import os

app = Flask(__name__)

#cohere_api_key = os.getenv("CO_API_KEY")
cohere_api_key = "s5yafntwVwUN7J108V11n9y4YceYj9ZvjAzBMAjI"
print(f"API Key: {cohere_api_key}")
co = cohere.Client(cohere_api_key)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.json

    # Get user inputs from the JSON data
    user_interests = data.get("interests")
    user_location = data.get("location")
    #user_interests = "legos, beyblade, star wars"
    #user_location = "Canada"

    # Use Cohere to generate content based on user inputs
    generation_response = co.generate(
        prompt=f'Please write a short story for nostalgia based on these parameters: {user_interests} {user_location}'
    )

    # Access the 'text' attribute to get the generated content
    generated_content = generation_response[0].text

    # Return the JSON response with the generated content
    return jsonify({"generated_content": generated_content})

if __name__ == '__main__':
    app.run(debug=True)