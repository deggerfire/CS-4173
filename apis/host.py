from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64
import requests

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
            aes_key = base64.b64encode(self.model.room_key[:-4].encode("utf-8"))
            aes = Fernet(aes_key)
            print(data)

            # room_key||name||ngrok||public_key||
            decrypted_data = aes.decrypt(data).decode("utf-8").split("||")

            if decrypted_data[0] != self.model.room_key or len(decrypted_data) != 4:
                return jsonify({"data": "ERROR||ERROR"})

            # Save their public key / ngrok link /user name
            self.model.Add_User(decrypted_data[1], decrypted_data[2], decrypted_data[3])

            # Send out new public key / name to other users
            for user in self.model.users:
                if user["name"] == decrypted_data[1]:
                    continue
                # SEND POST

            # Respond with all current user names and public keys
            res_str = ""
            for user in self.model.users:
                # Leave out new user of course
                if user["name"] == decrypted_data[1]:
                    continue
                res_str = user["name"] + "||" + user["public_key"]

            decrypted_res = aes.encrypt(res_str.encode("utf-8"))

            return jsonify({"data": decrypted_res.decode("utf-8")})

        @app.route("/message", methods=["POST"])
        def New_Message():
            # Decrypt message, save for host

            data = request.get_json()

            self.controller.Render_Message(data)

            # Send message out to other users

            return "New message"

        @app.route("/disconnect")
        def Disconnect_User():
            # Determine which user

            # clear out their data

            # Respond with a success

            return "Disconnect user"

    def run(self):
        app.run(debug=True, port=5173, use_reloader=False)
