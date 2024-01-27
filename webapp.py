from flask import Flask, make_response, redirect,render_template,request, send_from_directory

app = Flask(__name__)
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# tell Flask to use the above defined config
app.config.from_mapping(config)
@app.route("/")
def main():
    return render_template("home.html")