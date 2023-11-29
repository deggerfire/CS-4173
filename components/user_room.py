from tkinter import *
import threading
from tkinter import filedialog
import io
from PIL import Image, ImageTk
from apis import user
from models import user_room
import requests
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import apis.RSA_handler as RSA_handler


class Room:
    def __init__(
        self,
        window,
        user_ngrok_url,
        host_ngrok_url,
        room_password,
        username,
        message_label,
    ):
        self.window = window

        # Check that a username, password and URL were entered
        if username == "" or room_password == "" or host_ngrok_url == "":
            message_label.config(text="Failed to join room")
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

        # Get the AES key the hash function
        aes = Fernet(room_key)

        # Generates a RSA key pair of 2048 bits long
        rsa = RSA.generate(2048)

        # Encode the generate RSA public key (PEM encoded)
        public_key = rsa.publickey().export_key().decode("utf-8")

        # Build the JSON object that will be sent
        data = {
            "room_key": room_key.decode("utf-8"),
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

        try:
            # Send and receive form the server
            response = requests.post(url, json=data)
        except:
            message_label.config(text="Failed to join room")

        # Error check
        if response.status_code != 200:
            message_label.config(text="Failed to join room")
            return

        # Convert what the server sent to JSON
        res_json = response.json()

        # Check if we got into the room
        # TODO: Make this more funcationable !test!
        if res_json["data"] == ":(":
            message_label.config(text="Failed to join room")
            return

        # Decrypted the data inside of the returned JSON
        decrypted_data = json.loads(aes.decrypt(res_json["data"]).decode("utf-8"))

        # Make and store all of the users and their information
        users = []
        for key, value in decrypted_data.items():
            users.append({"name": key, "public_key": value})

        # Makes the user_room object used to keep track of users (the user_room in models)
        self.model = user_room.User_Room(
            user_ngrok_url, host_ngrok_url, username, users, rsa
        )

        # Start the GUI
        self.Create_Room(window)

        # Start a thread that handles communication
        user_api_t = threading.Thread(target=lambda: user.User_API(self.model, self))
        user_api_t.daemon = True
        user_api_t.start()

    # Clears the GUI
    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Sends a message to the other users
    def Send_Message(self, message):
        # JSON array to keep track of the messages
        messages = {}

        # Loop though all the users
        for user in self.model.users:
            # Encode the message using the other users public key
            public_key = RSA.import_key(user["public_key"])
            cipher = PKCS1_OAEP.new(public_key)
            messages[user["name"]] = base64.b64encode(
                cipher.encrypt(message.encode("utf-8"))
            ).decode("utf-8")

        # Put the message in JSON
        # TODO: string and encode the JSON
        data = {"name": self.model.username, "messages": messages}

        # Sent the message to the host who sends it to everyone
        url = self.model.host_ngrok_url + "/message"
        response = requests.post(url, json=data)

        # Error check
        if response.status_code != 200:
            self.window.quit().destroy()

    # Prints the messages on the screen
    def Render_Message(self, incomingMessage):
        # Error check the message
        self.list["state"] = "normal"
        if incomingMessage == None:
            message = self.input.get("1.0", "end").strip()
            self.Send_Message(message)
            self.input.replace("1.0", "end", "")
            self.list.insert(END, "\n" + "You: " + message)

        else:
            # Get the RSA key
            cipher = PKCS1_OAEP.new(self.model.rsa)
            # Decrypt the message and convert to utf-8
            message = cipher.decrypt(
                base64.b64decode((incomingMessage["message"].encode("utf-8")))
            ).decode("utf-8")
            # Get the user name
            username = incomingMessage["name"]
            # Add the message to the list of messages
            self.list.insert(END, "\n" + username + ": " + message)

        self.list["state"] = "disabled"

    def Upload_Image(self, incomingImage):
        if incomingImage == None:
            file_path = filedialog.askopenfilename()
            print(file_path)
            image = Image.open(file_path).resize((300, 300))
            photo = ImageTk.PhotoImage(image)

            image_frame = Frame(self.images_frame, bg="#191914")

            name = Label(
                image_frame,
                text="You",
                fg="#F1F1F1",
                bg="#191914",
            )
            name.pack()
            label = Label(
                self.images_frame, image=photo, height=100, width=100, bg="#191914"
            )
            label.image = photo
            label.pack()
            image_frame.pack()
            self.Send_Image(file_path)
        else:
            image = Image.open(io.BytesIO(base64.b64decode(incomingImage["image"])))
            photo = ImageTk.PhotoImage(image)

            image_frame = Frame(self.images_frame, bg="#191914")

            name = Label(
                image_frame,
                text=incomingImage["name"],
                fg="#F1F1F1",
                bg="#191914",
            )
            label = Label(
                image_frame,
                image=photo,
                height=100,
                width=100,
                bg="#191914",
            )
            label.image = photo
            label.pack()
            name.pack()
            image_frame.pack()

    def Send_Image(self, file_path):
        with Image.open(file_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_bytes = img_byte_arr.getvalue()

        images = {}

        for user in self.model.users:
            encoded_image = base64.b64encode(img_bytes).decode("utf-8")

            data = RSA_handler.encode(
                encoded_image.encode("utf-8"), RSA.import_key(user["public_key"])
            )

            images[user["name"]] = data

        data = {"uname": self.model.username, "images": images}

        url = self.model.host_ngrok_url + "/image"
        response = requests.post(url, json=data)

        if response.status_code != 200:
            print("FAILED TO SEND IMAGE TO")

    # The GUI for a user room
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

        chat_frame = Frame(frame, bg="#191914")
        images_frame = Frame(chat_frame, bg="#191914")

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
        send.pack(side=RIGHT, fill="x")
        btns_frame.pack()

        frame.pack()
