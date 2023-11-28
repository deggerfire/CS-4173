from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import io
import threading
from apis import host
from models import host_room
import requests
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives import hashes
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import apis.RSA_handler as RSA_handler


# The object with mainly the GUI components for a room host
class Room:
    def __init__(self, window, ngrok_url, username, room_password, message_label):
        self.window = window

        # Check that a username and password was entered
        # TODO: make min requirments for the password
        if username == "" or room_password == "":
            message_label.config(text="Failed to make room")
            return

        # Setup a SHA256 hash function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # Using SHA256 algorithm
            length=32,  # Needs to be of length 32 to be a key
            salt=b"",  # Super secure salt, just for early version
            iterations=480000,  # Recomended number of iterations
        )

        # Use the hash funcation to make a room key
        room_key = base64.urlsafe_b64encode(kdf.derive(bytes(room_password, "utf-8")))

        # Generates a RSA key pair of 2048 bits long
        rsa = RSA.generate(2048)

        # Create the GUI for the room
        self.Create_Room(
            window,
            ngrok_url,
            room_key,
        )

        # Setup the host room object
        self.model = host_room.Host_Room(ngrok_url, username, room_key, rsa)

        # Start a thread for the host api
        host_api_t = threading.Thread(target=lambda: host.Host_API(self.model, self))
        host_api_t.daemon = True
        host_api_t.start()

    # Clear the GUI
    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Sends messages to all chatters
    # TODO: some double coding between this and the one in user_room (comp) and new_message in host.py
    def Send_Message(self, message):
        for user in self.model.users:
            # Encode the message using each chatters public key
            public_key = RSA.import_key(user["public_key"])
            cipher = PKCS1_OAEP.new(public_key)
            eMessage = base64.b64encode(cipher.encrypt(message.encode("utf-8"))).decode(
                "utf-8"
            )

            # Put the data in a JSON
            data = {"name": self.model.username, "message": eMessage}

            # Send the message to the respective user
            url = user["ngrok"] + "/newMessage"
            print(url)
            response = requests.post(url, json=data)

            # Error check
            if response.status_code != 200:
                print("FAILED TO SEND MESSAGE TO: " + user["name"])

    # Prints out the messages
    # TODO: some double coding between this and the one in user_room (comp)
    def Render_Message(self, incomingMessage):
        # Error check
        self.list["state"] = "normal"
        if incomingMessage == None:
            message = self.input.get("1.0", "end").strip()
            self.Send_Message(message)
            self.input.replace("1.0", "end", "")
            self.list.insert(END, "\n" + "You: " + message)

        # Add the message
        else:
            print(incomingMessage)
            cipher = PKCS1_OAEP.new(self.model.rsa)
            message = cipher.decrypt(
                base64.b64decode((incomingMessage["message"].encode("utf-8")))
            ).decode("utf-8")
            username = incomingMessage["name"]
            self.list.insert(END, "\n" + username + ": " + message)

        self.list["state"] = "disabled"

    def Upload_Image(self, incomingImage):
        if incomingImage == None:
            file_path = filedialog.askopenfilename()
            print(file_path)
            image = Image.open(file_path).resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            label = Label(
                self.images_frame, image=photo, height=100, width=100, bg="#191914"
            )
            label.image = photo
            label.pack()
            self.Send_Image(file_path)
        else:
            image = Image.open(io.BytesIO(incomingImage.img_bytes))
            photo = ImageTk.PhotoImage(image)
            label = Label(
                self.images_frame, image=photo, height=100, width=100, bg="#191914"
            )
            label.image = photo
            label.pack()

    def Send_Image(self, file_path):
        with Image.open(file_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_bytes = img_byte_arr.getvalue()

        for user in self.model.users:
            public_key = RSA.import_key(user["public_key"])
            cipher = PKCS1_OAEP.new(public_key)

            data = {"data": {"image_name.jpg", img_bytes, "image/jpeg"}}

            url = user["ngrok"] + "/newImage"
            response = requests.post(url, json=data)

            if response.status_code != 200:
                print("FAILED TO SEND IMAGE TO: " + user["name"])

    # Setups the GUI for being in a chat room as a host
    # TODO: some double coding between this and the one in user_room (comp)
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

        chat_frame = Frame(frame)

        images_frame = Frame(chat_frame)

        list_frame = Frame(chat_frame)
        list_frame.pack(fill=BOTH, side=LEFT, expand=1)

        images_frame.pack(side=RIGHT)
        self.images_frame = images_frame

        chat_frame.pack(fill=BOTH)

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

        btns_frame = Frame(frame)

        upload = Button(
            btns_frame,
            text="Upload Image",
            fg="#191914",
            bg="#5AFAF0",
            font=("Lucida Sans", 20),
            activeforeground="#5AFAF0",
            activebackground="#24241E",
            height=70,
            border=1,
            relief="solid",
            command=lambda: self.Upload_Image(None),
        )
        upload.pack(side=LEFT)

        send = Button(
            btns_frame,
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
        send.pack(side=RIGHT, fill=X)
        btns_frame.pack()

        frame.pack()
