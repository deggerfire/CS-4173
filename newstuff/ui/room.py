from tkinter import *
import host
import threading


class Room:
    def __init__(self, window, type):
        self.window = window
        self.Create_Room(window)
        host.Host_API()
        # host_api_t = threading.Thread(target=host.Host_API())

    def Kill_UI(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def Render_Messages(self):
        for widget in self.list.winfo_children():
            widget.destroy()

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
        list = Frame(
            frame,
            bg="#24241E",
            pady=20,
            padx=20,
            height=400,
            width=100,
            border=1,
            relief="solid",
        )
        self.list = list  # KEEP TRACK OF LIST FRAME TO UPDATE AS MESSAGES COME IN
        list.pack(fill="x")
        text = Text(
            frame,
            height=4,
            fg="#F2F2F2",
            bg="#24241E",
            font=("Lucida Sans", 16),
            border=1,
            relief="solid",
        )
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
        )
        send.pack(fill="x")
        frame.pack()
