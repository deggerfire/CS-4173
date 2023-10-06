from tkinter import *

class Start:
    def __init__(self, window, start_app):
        self.Create_Start(window, start_app)
    
    def Enter(self, window, start_app):
        # CHECK CONNECTION HERE OR SOMETHING
        # IF CONNECTION GOOD start_app
        start_app(window)

    def Create_Start(self, window, start_app):
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.ip_var = StringVar()
        frame = Frame(window, bg="#191914",pady=20, padx=20)
        title = Label(frame, text='Vault Talk', fg='#5AFAF0', bg='#191914',font=('Lucida Sans', 32), pady=(5), padx=100)
        login_div = Frame(frame, bg='#191914', pady=10)
        username_label = Label(login_div, text='Username',font=('Lucida Sans', 20), bg='#191914', fg="#F2F2F2", pady=3)
        username = Entry(login_div, textvariable=self.username_var, width=50, font=('Lucida Sans', 16), bg="#24241E", border=0, fg="#F2F2F2")
        ip_label = Label(login_div, text='IP',font=('Lucida Sans', 20), bg='#191914', fg="#F2F2F2", pady=3)
        ip = Entry(login_div, textvariable=self.ip_var, width=50, font=('Lucida Sans', 16), bg="#24241E", border=0, fg="#F2F2F2")
        password_label = Label(login_div, text='Password', font=('Lucida Sans', 20), bg='#191914',fg="#F2F2F2", pady=3)
        password = Entry(login_div, textvariable=self.password_var, show="*", width=50,font=('Lucida Sans', 16), bg="#24241E", border=0, fg="#F2F2F2")
        login_btn = Button(frame, text="Enter", border=0, font=('Lucida Sans', 20),  bg='#191914', activeforeground='#50FAB4', fg="#F2F2F2", activebackground='#191914', command=lambda: self.Enter(window, start_app))
        username_label.pack()
        username.pack()
        ip_label.pack()
        ip.pack()
        password_label.pack()
        password.pack()
        title.pack()
        login_div.pack()
        login_btn.pack()
        frame.pack()