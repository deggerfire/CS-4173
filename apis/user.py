from flask import Flask, request
import base64
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import apis.RSA_handler as RSA_handler

app = Flask(__name__)


# Splits a string into length num chars (should be 256)
def chunkstring(string, length):
    return (string[0 + i : length + i] for i in range(0, len(string), length))


# Handles the communication between machines
class User_API:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.Set_Routes()
        self.run()

    # Where inbound messages come to
    def Set_Routes(self):
        @app.route("/newMessage", methods=["POST"])
        # Handles when a new message shows up
        def newMessage():
            # Get the json from the request
            data = request.get_json()

            # Send the message to be rendered
            self.controller.Render_Message(
                {"name": data["name"], "message": data["message"]}
            )

            # Reply to the request
            return "Success"

        @app.route("/newUser", methods=["POST"])
        # Handles a new user being added to the room
        def newUser():
            # Get the data from JSON
            data = request.get_json()["data"]

            # Decode the message
            # cipher = PKCS1_OAEP.new(self.model.rsa)
            new_user = json.loads(RSA_handler.decode(data, self.model.rsa))

            # Save new user
            self.model.Add_User(new_user["name"], new_user["public_key"])

            return "Success"

        @app.route("/newImage", methods=["POST"])
        def newImage():
            data = request.get_json()
            image = RSA_handler.decode(data["image"], self.model.rsa)

            self.controller.Upload_Image({"image": image})

            return "Success"

    def run(self):
        app.run(debug=True, port=5173, use_reloader=False)
