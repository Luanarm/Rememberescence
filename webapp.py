from flask import Flask, render_template, request, jsonify
import cohere

app = Flask(__name__)

cohere_api_key = "s5yafntwVwUN7J108V11n9y4YceYj9ZvjAzBMAjI"
co = cohere.Client(cohere_api_key)

# Prompt add-ons
# Do not include
DNI = "Do not include generic narrations like 'sure here it is' or 'let me know' at the beginning or end."
# Address user as 'you'
address_user = "Address the user as 'you'."

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.json

    user_interests = data.get("interests")
    user_location = data.get("location")
    user_age = data.get("age")
    user_friends = data.get("friends")

    parameters = f'Friends:{user_friends}, Interests: {user_interests}, Location: {user_location}.'
    generation_response = co.generate(
        prompt=f'Please write a nostalgic short story about the users childhood based on these parameters: {parameters} {address_user} {DNI}'
    )

    generated_content = generation_response[0].text

    return jsonify({"generated_content": generated_content})

@app.route("/refine", methods=["POST"])
def refine_story():
    data = request.json
    generated_content = data.get("generated_content")
    new_prompt = f'Based on this short story, generate 1 short question that is maximum 10 words long to probe the user deeper: {generated_content}. {address_user} {DNI}'
    new_question_response = co.generate(prompt=new_prompt)  
    new_question = new_question_response[0].text
    return jsonify({"new_question": new_question})

@app.route("/refined", methods=["POST"])
def refined_output():
    data = request.json
    generated_content = data.get("generated_content")
    new_question = data.get("new_question")
    new_question_input = data.get("new_question_input")

    refined_prompt = f'Based on the question: {new_question} and the users answer: {new_question_input}, change and modify: {generated_content} with the same amount of words. {address_user} {DNI}'
    new_refined_response = co.generate(prompt=refined_prompt)
    refined_result = new_refined_response[0].text
    print(refined_result)

    return jsonify({"refined_result": refined_result})

if __name__ == '__main__':
    app.run(debug=True)
