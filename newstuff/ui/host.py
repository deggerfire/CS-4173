from flask import Flask, request

app = Flask(__name__)


class Host_API:
    def __init__(self):
        self.app = app
        self.Set_Routes()
        self.run()

    def Set_Routes(self):
        @app.route("/newUser")
        def newUser():
            # Verify user

            # Save their public key / ngrok link /user info

            # Send out new public key / name to other users

            # Respond with all current user names and public keys

            print(request)
            return "Hello, World!"

        @app.route("/message")
        def newMessage():
            # Decrypt message, save for host

            # Send message out to other users

            print("new message")

            return "New message"

        @app.route("/disconnect")
        def disconnectUser():
            # Determine which user

            # clear out their data

            # Respond with a success

            return "Disconnect user"

    def run(self):
        app.run(debug=True, port=5173)
