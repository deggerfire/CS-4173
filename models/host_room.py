# user:
#   name: ""
#   ngrok: ""
#   publicKey: ""

# Object to keep track of room deatils and who is in the room
class Host_Room:
    # Set the room host and other details about the room
    def __init__(self, ngrok_url, username, room_key, rsa):
        self.ngrok_url = ngrok_url
        self.room_key = room_key
        self.users = []
        self.messages = []
        self.username = username
        self.rsa = rsa

    # Addes a new user to the room
    def Add_User(self, name, ngrok, public_key):
        self.users.append({"name": name, "ngrok": ngrok, "public_key": public_key})
