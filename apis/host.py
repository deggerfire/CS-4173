from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64
import requests
import json

app = Flask(__name__)


class Host_API:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.Set_Routes()
        self.run()

    def Set_Routes(self):
        @app.route("/newUser", methods=["POST"])
        def New_User():
            # Verify user
            data = request.get_json()["data"]

            # AES Key
            aes = Fernet(self.model.room_key)

            decrypted_data = json.loads(aes.decrypt(data).decode("utf-8"))
            print(decrypted_data)

            if decrypted_data["room_key"] != self.model.room_key.decode("utf-8"):
                return jsonify({"data": ":("})

            # Save their public key / ngrok link /user name
            self.model.Add_User(
                decrypted_data["username"],
                decrypted_data["ngrok_url"],
                decrypted_data["public_key"],
            )

            # Send out new public key / name to other users
            for user in self.model.users:
                if user["name"] == decrypted_data["username"]:
                    continue

                data = {
                    "name": decrypted_data["username"],
                    "public_key": decrypted_data["public_key"],
                }

                # response = request.post(user["ngrok"] + "/newUser", json=data)

            # Respond with all current user names and public keys
            data = {
                self.model.username: self.model.rsa.publickey()
                .export_key()
                .decode("utf-8")
            }
            for user in self.model.users:
                # Leave out new user of course
                if user["name"] == decrypted_data["username"]:
                    continue
                data[user["name"]] = user["public_key"]

            encrypted_res = aes.encrypt(json.dumps(data).encode("utf-8"))

            return jsonify({"data": encrypted_res.decode("utf-8")})

        @app.route("/message", methods=["POST"])
        def New_Message():
            # Decrypt message, save for host

            data = request.get_json()

            # Send message out to other users
            for key, value in data.messages:
                # keep the host encrypted message for host
                if key == self.model.username.items():
                    self.controller.Render_Message(
                        {"name": data["name"], "message": value}
                    )

            return "New message"

        @app.route("/disconnect")
        def Disconnect_User():
            # Determine which user

            # clear out their data

            # Respond with a success

            return "Disconnect user"

    def run(self):
        app.run(debug=True, port=5173, use_reloader=False)
