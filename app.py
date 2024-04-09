from flask import Flask, render_template, request, jsonify
from chatbot import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("This is the query: ", msg)
    response = main(msg)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8080)
