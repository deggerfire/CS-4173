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

        # AES setup
        aes = Fernet(room_key)

        # RSA setup
        rsa = RSA.generate(2048)

        # RSA public (PEM encoded)
        public_key = rsa.publickey().export_key().decode("utf-8")

        data = {
            "room_key": room_key,
            "username": username,
            "ngrok_url": user_ngrok_url,
            "public_key": public_key,
        }

        req_str = json.dumps(data)

        encrypted_data = aes.encrypt(req_str.encode("utf-8"))

        url = host_ngrok_url + "/newUser"

        data = {"data": encrypted_data.decode("utf-8")}

        response = requests.post(url, json=data)

        if response.status_code != 200:
            return

        res_json = response.json()

        if res_json["data"] == ":(":
            return

        decrypted_data = json.loads(aes.decrypt(res_json["data"]).decode("utf-8"))
        print(decrypted_data)

        users = []

        for key, value in decrypted_data.items():
            users.append({"name": key, "public_key": value})

        self.window = window

        self.model = user_room.User_Room(
            user_ngrok_url, host_ngrok_url, username, users, rsa
        )

        self.Create_Room(window)

    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def Send_Message(self, message):
        messages = {}

        for user in self.model.users:
            public_key = RSA.import_key(user["public_key"])
            cipher = PKCS1_OAEP.new(public_key)
            messages[user["name"]] = cipher.encrypt(message.encode("utf-8")).decode(
                "utf-8"
            )

        data = {"name": self.model.username, "messages": messages}
        print(data)

        url = self.model.host_ngrok_url + "/message"

        response = requests.post(url, json=data)

        print(response)
        print("Status: ", response.status_code)

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
            message = incomingMessage["message"]
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
