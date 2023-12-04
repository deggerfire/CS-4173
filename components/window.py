from tkinter import *
from components import menu

# Black - #191914
# Dark grey - #24241E
# Blue - #5AFAF0
# Yellowy-green - #BEE6BE
# Green - #50FAB4
# White - #F2F2F2

# Creates the main window and does general formatting
def Create_Window():
    window = Tk()
    window.title("Super Stealth Chat")
    window.configure(bg="#191914", pady=30)
    window.geometry("1300x704")
    window.minsize(width=896, height=704)
    window.iconphoto(True, icon := PhotoImage(file="components/imgs/icon.png"))
    return window

# Calls all the setup functions (more or less init)
def Start(ngrok_url):
    window = Create_Window()
    # Create the menu
    menu.Menu(window, ngrok_url)
    return window
