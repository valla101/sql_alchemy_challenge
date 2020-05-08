from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    return "List of all directories<br>"
    "Test 1"