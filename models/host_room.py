# user:
#   name: ""
#   ngrok: ""
#   publicKey: ""


class Host_Room:
    def __init__(self, ngrok_url):
        self.ngrok_url = ngrok_url
        self.room_key = ngrok_url[:32]
        self.users = []
        self.messages = []
        self.username

    def Add_User(self, name, ngrok, public_key):
        self.users.append({"name": name, "ngrok": ngrok, "public_key": public_key})
