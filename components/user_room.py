from tkinter import *
import threading
from apis import user
from models import user_room
import requests
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json


class Room:
    def __init__(self, window, user_ngrok_url, host_ngrok_url, room_key, username):
        self.window = window

        # Get the AES key from what the user input
        aes = Fernet(room_key)

        # Generates a RSA key pair of 2048 bits long
        rsa = RSA.generate(2048)

        # Encode the generate RSA public key (PEM encoded)
        public_key = rsa.publickey().export_key().decode("utf-8")

        # Build the JSON object that will be sent
        data = {
            "room_key": room_key,
            "username": username,
            "ngrok_url": user_ngrok_url,
            "public_key": public_key,
        }

        # Convert the JSON to a string
        req_str = json.dumps(data)

        # Encode the JSON
        encrypted_data = aes.encrypt(req_str.encode("utf-8"))

        # Set the URL
        url = host_ngrok_url + "/newUser"

        # Make a JSON object to hold the data
        data = {"data": encrypted_data.decode("utf-8")}

        # Send and receive form the server
        response = requests.post(url, json=data)

        # Error check
        if response.status_code != 200:
            return

        # Convert what the server sent to JSON
        # TODO: check for valid JSON
        res_json = response.json()

        # Make sure this is data
        if res_json["data"] == ":(":
            return

        # Decrypted the data inside of the returned JSON
        decrypted_data = json.loads(aes.decrypt(res_json["data"]).decode("utf-8"))
        print(decrypted_data)

        # Make and store all of the users and their information
        # TODO: error here when there is to many users
        users = []
        for key, value in decrypted_data.items():
            users.append({"name": key, "public_key": value})

        self.model = user_room.User_Room(
            user_ngrok_url, host_ngrok_url, username, users, rsa
        )

        self.Create_Room(window)

        user_api_t = threading.Thread(target=lambda: user.User_API(self.model, self))
        user_api_t.daemon = True
        user_api_t.start()

    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def Send_Message(self, message):
        messages = {}

        for user in self.model.users:
            public_key = RSA.import_key(user["public_key"])
            cipher = PKCS1_OAEP.new(public_key)
            messages[user["name"]] = base64.b64encode(
                cipher.encrypt(message.encode("utf-8"))
            ).decode("utf-8")

        data = {"name": self.model.username, "messages": messages}
        print(data)

        url = self.model.host_ngrok_url + "/message"

        response = requests.post(url, json=data)

        if response.status_code != 200:
            self.window.quit().destroy()

    def Render_Message(self, incomingMessage):
        self.list["state"] = "normal"
        if incomingMessage == None:
            message = self.input.get("1.0", "end").strip()
            self.Send_Message(message)
            self.input.replace("1.0", "end", "")
            self.list.insert(END, "\n" + "You: " + message)

        else:
            print(incomingMessage)
            cipher = PKCS1_OAEP.new(self.model.rsa)
            message = cipher.decrypt(
                base64.b64decode((incomingMessage["message"].encode("utf-8")))
            ).decode("utf-8")
            username = incomingMessage["name"]
            self.list.insert(END, "\n" + username + ": " + message)

        self.list["state"] = "disabled"

    def Create_Room(self, window):
        self.Kill_UI()
        frame = Frame(window, bg="#191914", pady=15, padx=15)
        title = Label(
            frame,
            text="Chat Room",
            fg="#5AFAF0",
            bg="#191914",
            font=("Lucida Sans", 32),
            pady=(5),
            padx=100,
        )
        title.pack()

        list_frame = Frame(frame)
        list_frame.pack(fill=BOTH, expand=1)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        list = Text(
            list_frame,
            yscrollcommand=scrollbar.set,
            state=DISABLED,
            fg="#F2F2F2",
            bg="#24241E",
            font=("Lucida Sans", 16),
            border=1,
            relief="solid",
            height=15,
        )
        list.pack(side=LEFT, fill=X)
        self.list = list

        text = Text(
            frame,
            height=4,
            fg="#F2F2F2",
            bg="#24241E",
            font=("Lucida Sans", 16),
            border=1,
            relief="solid",
        )
        self.input = text
        text.pack()

        send = Button(
            frame,
            text="Send",
            fg="#191914",
            bg="#5AFAF0",
            font=("Lucida Sans", 20),
            activeforeground="#5AFAF0",
            activebackground="#24241E",
            height=70,
            border=1,
            relief="solid",
            command=lambda: self.Render_Message(None),
        )
        send.pack(fill="x")

        frame.pack()
