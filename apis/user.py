from flask import Flask, request
import base64
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)


class User_API:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.Set_Routes()
        self.run()

    def Set_Routes(self):
        @app.route("/newMessage", methods=["POST"])
        def newMessage():
            data = request.get_json()

            self.controller.Render_Message(
                {"name": data["name"], "message": data["message"]}
            )

            return "Success"

        @app.route("/newUser", methods=["POST"])
        def newUser():
            data = request.get_json()["data"]
            print(data)

            # Save new user
            cipher = PKCS1_OAEP.new(self.model.rsa)
            new_user = json.loads(
                cipher.decrypt(base64.b64decode((data.encode("utf-8")))).decode("utf-8")
            )

            self.model.Add_User(new_user["name"], new_user["public_key"])

            return "Success"

    def run(self):
        app.run(debug=True, port=5173, use_reloader=False)
