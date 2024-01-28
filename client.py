import requests
import json

# Define the Flask server URL
SERVER_URL = "http://127.0.0.1:5000"

def generate_content(interests, location, age, genre):
    # Define the request payload
    payload = {
        "interests": interests,
        "location": location,
        "age": age,
        "genre": genre
    }

    # Send a POST request to the Flask server's /generate endpoint
    response = requests.post(f"{SERVER_URL}/generate", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("Generated Content:")
        print(data.get("generated_content"))
        if data.get("playlist_created"):
            print("Playlist created successfully!")
        else:
            print("Playlist creation failed.")
    else:
        print("Failed to generate content. Status code:", response.status_code)

if __name__ == "__main__":
    # Example usage
    generate_content("legos, beyblade, star wars", "Canada", "30", "rock")
