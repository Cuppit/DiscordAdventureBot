"""

This is a simple module whose sole purpose is to provide GUI file selection
functionality.

Quick employment is courtesy of example tutorials by Mokhtar Ebrahim at likeGeeks.com:
https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Handle-button-click-event

"""

import gui  #For implementing EasyTkinter for loading the bot's token.  It's safer this way, and prevents
            #accidental sharing of your bot's
from tkinter import filedialog
from tkinter import Tk
from tkinter import Menu
from tkinter import Label

'''
This opens a GUI window presented to the user for selection of a 
bot token stored in a plaintext file on the user's filesystem.  It
returns a string which is the token found.  If a token is not found,
it returns an error message string, as well as prints an error to the console.
'''


def token_select_dialog():
    token: str = ""
    window = Tk()
    window.title("Discord Adventure Bot")
    window.iconbitmap = "botloadericon.png"
    lbl = Label(window, text="To start the bot, a token needs to be loaded.\n\n"
                             "This module expects the token to be in a plaintext file, \n"
                             "with the only line of content being the token itself.\n\n"
                             "Click 'File -> Select Token' to choose a token from your file system.", font=("Arial Bold", 16))

    lbl.grid(column=0, row=0)
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)

    def choosefile():
        filepath = filedialog.askopenfilename(filetypes=(("Token file", "*.token"), ("Text files", "*.txt"), ("all files", "*.*")))

        with open(filepath, mode='r') as file:
            nonlocal token
            token=file.read()

        window.destroy() #We can shut down the GUI now that the bot is running.


    new_item.add_command(label='Load Token', command=choosefile)
    menu.add_cascade(label='File', menu=new_item)
    window.config(menu=menu)
    window.mainloop()
    return token

"""
menu.add_command(label='File')
window.config(menu=menu)

window = gui.Window("Please select where your Bot token is stored.  This module expects loads your token from a plaintext file that contains one line containing your bot's token.")
btn = window.add_button("Click Me")
gui.on("btnPress", btn, lambda: print("Button Pressed."))
window.start()
"""
