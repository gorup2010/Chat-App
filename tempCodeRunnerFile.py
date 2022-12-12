
import tkinter
import threading
from functools import partial
import random
import tkinter.scrolledtext
import socket

chat_win = tkinter.Toplevel()
chat_win.title(f" đang chat với")

text_area = tkinter.scrolledtext.ScrolledText(chat_win)
text_area.config(font=('arial', 14), height=15, width=50)
text_area.pack(padx=4, pady=4)
#text_area['state'] = 'disabled'

msg_lbl = tkinter.Label(chat_win, font=5, text="Nhắn tin: ")
msg_lbl.pack(padx=4, pady=4)

input_area = tkinter.Text(chat_win, font=('arial', 14), height=2, width=50)
input_area.pack(padx=4, pady=4)

send_msg_btn = tkinter.Button(chat_win, text="Gửi", font=5, width=10)
send_msg_btn.pack(padx=4, pady=4)

chat_win.mainloop()