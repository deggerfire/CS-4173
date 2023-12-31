from tkinter import *
from components import host_room, user_room

# The objects that are in the window
class Menu:
    def __init__(self, window, ngrok_url):
        self.window = window
        self.ngrok_url = ngrok_url
        self.User_Type()

    # Deletes all the content in the window
    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # The GUI for selecting being a user or a host
    def User_Type(self):
        self.Kill_UI()
        frame = Frame(self.window, bg="#191914", pady=20, padx=20)
        title = Label(
            frame,
            text="Super Stealth Chat",
            fg="#5AFAF0",
            bg="#191914",
            font=("Lucida Sans", 40),
            pady=(5),
            padx=100,
        )
        host_btn = Button(
            frame,
            text="Host a room",
            border=0,
            font=("Lucida Sans", 24),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F1F1F1",
            activebackground="#191914",
            command=lambda: self.Host_Menu(),
        )
        join_btn = Button(
            frame,
            text="Join a room",
            border=0,
            font=("Lucida Sans", 24),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F1F1F1",
            activebackground="#191914",
            command=lambda: self.Join_Menu(),
        )
        title.pack()
        host_btn.pack()
        join_btn.pack()
        frame.pack()

    # The GUI for making a chat room as a host
    def Host_Menu(self):
        self.Kill_UI()
        self.username_var = StringVar()
        self.room_password_var = StringVar()
        frame = Frame(self.window, bg="#191914", pady=20, padx=20)
        title = Label(
            frame,
            text="Super Stealth Chat",
            fg="#5AFAF0",
            bg="#191914",
            font=("Lucida Sans", 32),
            pady=(5),
            padx=100,
        )
        login_div = Frame(frame, bg="#191914", pady=10)
        username_label = Label(
            login_div,
            text="Username",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F2F2F2",
            pady=3,
        )
        username = Entry(
            login_div,
            textvariable=self.username_var,
            width=50,
            font=("Lucida Sans", 16),
            bg="#24241E",
            border=0,
            fg="#F2F2F2",
        )
        room_password_label = Label(
            login_div,
            text="Password",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F2F2F2",
            pady=3,
        )
        room_password = Entry(
            login_div,
            textvariable=self.room_password_var,
            width=50,
            font=("Lucida Sans", 16),
            bg="#24241E",
            border=0,
            fg="#F2F2F2",
        )
        message_label = Label(
            login_div,
            text="",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F20000",
            pady=3,
        )
        start_btn = Button(
            frame,
            text="Start",
            border=0,
            font=("Lucida Sans", 20),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F2F2F2",
            activebackground="#191914",
            command=lambda: host_room.Room(
                self.window, self.ngrok_url, self.username_var.get(), self.room_password_var.get(), message_label
            ),
        )
        back_btn = Button(
            frame,
            text="Back",
            border=0,
            font=("Lucida Sans", 20),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F2F2F2",
            activebackground="#191914",
            command=lambda: self.User_Type(),
        )
        username_label.pack()
        username.pack()
        room_password_label.pack()
        room_password.pack()
        title.pack()
        login_div.pack()
        message_label.pack()
        start_btn.pack()
        back_btn.pack()
        frame.pack()

    # The GUI for joining a chat room
    def Join_Menu(self):
        self.Kill_UI()
        self.username_var = StringVar()
        self.room_key_var = StringVar()
        self.host_ngrok_url_var = StringVar()
        frame = Frame(self.window, bg="#191914", pady=20, padx=20)
        title = Label(
            frame,
            text="Super Stealth Chat",
            fg="#5AFAF0",
            bg="#191914",
            font=("Lucida Sans", 32),
            pady=(5),
            padx=100,
        )
        login_div = Frame(frame, bg="#191914", pady=10)
        username_label = Label(
            login_div,
            text="Username",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F2F2F2",
            pady=3,
        )
        username = Entry(
            login_div,
            textvariable=self.username_var,
            width=50,
            font=("Lucida Sans", 16),
            bg="#24241E",
            border=0,
            fg="#F2F2F2",
        )
        ngrok_url_label = Label(
            login_div,
            text="Room Url",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F2F2F2",
            pady=3,
        )
        ngrok_url = Entry(
            login_div,
            textvariable=self.host_ngrok_url_var,
            # show="*",
            width=50,
            font=("Lucida Sans", 16),
            bg="#24241E",
            border=0,
            fg="#F2F2F2",
        )

        room_key_label = Label(
            login_div,
            text="Room Key",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F2F2F2",
            pady=3,
        )
        room_key = Entry(
            login_div,
            textvariable=self.room_key_var,
            # show="*",
            width=50,
            font=("Lucida Sans", 16),
            bg="#24241E",
            border=0,
            fg="#F2F2F2",
        )
        message_label = Label(
            login_div,
            text="",
            font=("Lucida Sans", 20),
            bg="#191914",
            fg="#F20000",
            pady=3,
        )
        login_btn = Button(
            frame,
            text="Enter",
            border=0,
            font=("Lucida Sans", 20),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F2F2F2",
            activebackground="#191914",
            command=lambda: user_room.Room(
                self.window,
                self.ngrok_url,
                self.host_ngrok_url_var.get(),
                self.room_key_var.get(),
                self.username_var.get(),
                message_label,
            ),
        )
        back_btn = Button(
            frame,
            text="Back",
            border=0,
            font=("Lucida Sans", 20),
            bg="#191914",
            activeforeground="#50FAB4",
            fg="#F2F2F2",
            activebackground="#191914",
            command=lambda: self.User_Type(),
        )
        username_label.pack()
        username.pack()
        ngrok_url_label.pack()
        ngrok_url.pack()
        room_key_label.pack()
        room_key.pack()
        title.pack()
        login_div.pack()
        login_btn.pack()
        back_btn.pack()
        message_label.pack()
        frame.pack()
