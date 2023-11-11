class User_Room:
    def __init__(self, user_ngrok_url, host_ngrok_url, username, users, rsa):
        self.ngrok_url = user_ngrok_url
        self.host_ngrok_url = host_ngrok_url
        self.users = users
        self.messages = []
        self.username = username
        self.rsa = rsa

    def Add_User(self, name, public_key):
        self.users.append({"name": name, "public_key": public_key})
