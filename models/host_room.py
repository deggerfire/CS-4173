# user:
#   name: ""
#   ngrok: ""
#   publicKey: ""


class Host_Room:
    def __init__(self, ngrok_url, username, room_key, rsa):
        self.ngrok_url = ngrok_url
        self.room_key = room_key
        self.users = []
        self.messages = []
        self.username = username
        self.rsa = rsa

    def Add_User(self, name, ngrok, public_key):
        self.users.append({"name": name, "ngrok": ngrok, "public_key": public_key})
