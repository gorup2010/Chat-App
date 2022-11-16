import tkinter
import threading
from tkinter import simpledialog
import tkinter.scrolledtext
import socket

main = tkinter.Tk()
main.title('Chat Application')

frm_friend = tkinter.Frame(master=main, height=200, width=200, bg='blue')
frm_friend.pack(side=tkinter.LEFT)

frm_onl_user = tkinter.Frame(master=main, height=200, width=200, bg='red')
frm_onl_user.pack(side=tkinter.LEFT)

main.mainloop()