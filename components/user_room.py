from tkinter import *
import threading
from apis import host
from models import user_room
import requests
from cryptography.fernet import Fernet
import base64


class Room:
    def __init__(self, window, ngrok_url, room_key, username):
        aes_key = base64.b64encode(room_key[:32].encode("utf-8"))
        aes = Fernet(aes_key)

        req_str = room_key + "||" + username + "||" + ngrok_url + "||" + "123"

        encrypted_data = aes.encrypt(req_str.encode("utf-8"))

        url = room_key + "/newUser"

        data = {"data": encrypted_data.decode("utf-8")}

        response = requests.post(url, json=data)

        if response.status_code != 200:
            return

        json = response.json()

        if json["data"] == "ERROR||ERROR":
            return

        decrypted_data = aes.decrypt(json["data"]).decode("utf-8").split("][")

        users = []

        for data in decrypted_data:
            user = decrypted_data.split("||")
            users.append({"name": user[0], "public_key": user[1]})

        self.window = window

        self.model = user_room.Uost_Room(ngrok_url, users)

        self.Create_Room(window)

    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def Render_Message(self, incomingMessage):
        self.list["state"] = "normal"
        if incomingMessage == None:
            message = self.input.get("1.0", "end").strip()
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
