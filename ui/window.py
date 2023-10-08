from tkinter import *
import start
import room

# Black - #191914
# Dark grey - #24241E
# Blue - #5AFAF0
# Yellowy-green - #BEE6BE
# Green - #50FAB4
# White - #F2F2F2

def Create_Window():
    window = Tk()
    window.title('Vault Talk')
    window.configure(bg='#191914', pady=30)
    window.geometry('896x704')
    window.minsize(width=896, height=704)
    window.iconphoto(True, icon := PhotoImage(file='ui/imgs/icon.png'))
    return window

def Placeholder():
    pass
instance = {}

window = Create_Window()
# start.Start(window, Placeholder)
room.Room(window, instance)
window.mainloop()