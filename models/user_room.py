class User_Room:
    def __init__(self, ngrok_url, users):
        self.ngrok_url = ngrok_url
        self.users = users
        self.messages = []
