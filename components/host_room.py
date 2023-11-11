from tkinter import *
import threading
from apis import host
from models import host_room
import requests
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class Room:
    def __init__(self, window, ngrok_url, username):
        self.window = window

        room_key = Fernet.generate_key()
        rsa = RSA.generate(2048)

        self.Create_Room(
            window,
            ngrok_url,
            room_key,
        )

        self.model = host_room.Host_Room(ngrok_url, username, room_key, rsa)

        host_api_t = threading.Thread(target=lambda: host.Host_API(self.model, self))
        host_api_t.daemon = True
        host_api_t.start()

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
            print(incomingMessage)
            cipher = PKCS1_OAEP.new(self.model.rsa)
            message = cipher.decrypt(
                base64.b64decode((incomingMessage["message"].encode("utf-8")))
            ).decode("utf-8")
            username = incomingMessage["name"]
            self.list.insert(END, "\n" + username + ": " + message)

        self.list["state"] = "disabled"

    def Create_Room(self, window, ngrok_url, room_key):
        self.Kill_UI()
        frame = Frame(window, bg="#191914", pady=15, padx=15)
        key = Text(
            frame,
            fg="#F1F1F1",
            bg="#191914",
            font=("Lucida Sans", 14),
            height=1,
            border=0,
        )
        key.insert(
            END,
            "Room Key: " + room_key.decode("utf-8"),
        )
        key["state"] = "disabled"
        key.pack()
        url = Text(
            frame,
            fg="#F1F1F1",
            bg="#191914",
            font=("Lucida Sans", 14),
            height=1,
            border=0,
        )
        url.insert(
            END,
            "Room Url: " + ngrok_url,
        )
        url["state"] = "disabled"
        url.pack()
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
