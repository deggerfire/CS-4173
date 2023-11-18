from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import requests
import json

app = Flask(__name__)


# The API for a host room which handles encoding and moving messages around
class Host_API:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.Set_Routes()
        self.run()

    def Set_Routes(self):
        @app.route("/newUser", methods=["POST"])
        # Checks and adds a new user to the room
        def New_User():
            # Get the JSON from the request
            data = request.get_json()["data"]
            print("Encrypted Request Data: ")
            print(data)# TODO: print out for debugging
            # Get the AES Key
            aes = Fernet(self.model.room_key)

            # Decrypted the inbound message and convert it to json
            try:
                decrypted_data = json.loads(aes.decrypt(data).decode("utf-8"))
            except:# If an error occurs then it is not a vaild user
                return jsonify({"data": ":("})

            print("Decrypted Request Data: ")
            print(decrypted_data) # TODO: print out for debugging

            # Save the new users information
            self.model.Add_User(
                decrypted_data["username"],
                decrypted_data["ngrok_url"],
                decrypted_data["public_key"],
            )

            # Send out new users information to other users
            for user in self.model.users:
                # Skip the host user
                if user["name"] == decrypted_data["username"]:
                    continue

                # Get the new user info (name, public key)
                user_info = {
                    "name": decrypted_data["username"],
                    "public_key": decrypted_data["public_key"],
                }

                # Convert the new user info to a json string
                user_info_str = json.dumps(user_info)

                # Get and load the public key
                public_key = RSA.import_key(user["public_key"])
                cipher = PKCS1_OAEP.new(public_key)

                # Encrypt the data
                data = {
                    "data": base64.b64encode(
                        cipher.encrypt(user_info_str.encode("utf-8"))
                    ).decode("utf-8")
                }

                # Send the encrypted user info
                response = request.post(user["ngrok"] + "/newUser", json=data)

                # Error check
                if response.status_code != 200:
                    print("ERROR SENDING NEW USER INFO TO CURRENT USERS")

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

            # Encrypt the message
            encrypted_res = aes.encrypt(json.dumps(data).encode("utf-8"))

            return jsonify({"data": encrypted_res.decode("utf-8")})

        @app.route("/message", methods=["POST"])
        # Receives and sends a message to all users in the chat room
        # TODO: error when two users send a message at the same time
        def New_Message():
            # Get the data out of the JSON
            data = request.get_json()
            print(data)

            # Loop though the messages that need to be sent
            # TODO: when/if encoding JSON string means it will need to be decoded here, might be a problem
            for key, value in data["messages"].items():
                # Keep the host encrypted message for host
                if key == self.model.username:
                    self.controller.Render_Message(
                        {"name": data["name"], "message": value}
                    )
                    continue

                # Send the other messages to the respective user
                forwarded_data = {"name": data["name"], "message": value}
                response = request.post(
                    self.model.users[key]["ngrok"] + "/newUser", json=forwarded_data
                )

                # Error check
                if response.status_code != 200:
                    print("MESSAGE NOT SENT TO: " + self.model.users[key]["name"])

            return "Success"

        @app.route("/disconnect")
        # Disconnects a user the from the chat
        # TODO: dew it
        def Disconnect_User():
            # Determine which user

            # clear out their data

            # Respond with a success

            return "Disconnect user"

    def run(self):
        app.run(debug=True, port=5173, use_reloader=False)
