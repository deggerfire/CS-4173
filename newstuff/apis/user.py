from flask import Flask, request

app = Flask(__name__)


@app.route("/newMessage")
def newMessage():
    # Save message

    # Respond with success

    print(request)
    return "Hello, World!"


@app.route("/newUser")
def newUser():
    # Save new user

    # Response with success

    return "new user"


def run(room):
    app.run(debug=True, port=3000)
