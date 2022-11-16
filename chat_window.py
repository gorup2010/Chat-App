import tkinter
import threading
from tkinter import simpledialog
import tkinter.scrolledtext
import socket

username = "lauhoi"

chat = tkinter.Toplevel(master=None)
chat.title(username)

txt_area = tkinter.scrolledtext.ScrolledText(master=chat)
txt_area.config(borderwidth= 4, relief="groove", state="disabled")
txt_area.pack(pady=5, fill=tkinter.X)

lbl_input = tkinter.Label(master=chat, text='Nhập tin nhắn vào đây', font=3)
lbl_input.pack(pady=5)

txt_input = tkinter.Entry(master=chat, background='white', font=10, width=50)
txt_input.pack(pady=5)

btn_send = tkinter.Button(master=chat, text='Gửi', width=10, font=3)
btn_send.pack(pady=5)

chat.mainloop()