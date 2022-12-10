import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext
from tkinter import ttk

class main_window:
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.title(f'Chào mừng trở lại')

        self.create_main_frame()
        self.create_friend_frame()
        self.create_onl_user_frame()
        self.create_fr_request_frame()
        self.create_send_fr_request_frame()

        self.current_fr = None

        self.main.protocol("WM_DELETE_WINDOW", self.log_out)

    def start(self):
        self.main_fr.grid(row=0, column=0)
        self.main.mainloop()

    def create_main_frame(self):
        self.main_fr = tkinter.Frame(self.main)

        self.btn_friend = tkinter.Button(self.main_fr, text="Bạn bè", command=self.show_friend, font=6)
        self.btn_friend.grid(row=0,column=0,sticky='nwes')

        self.btn_onl_user = tkinter.Button(self.main_fr, text="Người dùng online", command=self.show_onl_user, font=6)
        self.btn_onl_user.grid(row=0,column=1,sticky='nwes')

        self.btn_fr_request = tkinter.Button(self.main_fr, text="Lời mời kết bạn", command=self.show_fr_request, font=6)
        self.btn_fr_request.grid(row=1,column=0,sticky='nwes')

        self.btn_send_fr_request = tkinter.Button(self.main_fr, text="Lời mời kết bạn đã gửi", command=self.show_send_fr_request, font=6)
        self.btn_send_fr_request.grid(row=1,column=1,sticky='nwes')

        self.btn_log_out = tkinter.Button(self.main_fr, text="Đăng xuất", command=self.log_out, font=6)
        self.btn_log_out.grid(row=2,column=0, sticky='nwes')

        self.main_fr.columnconfigure(index=0, weight=1)
        self.main_fr.columnconfigure(index=1, weight=1)

        self.main_fr.rowconfigure(index=0, weight=1)
        self.main_fr.rowconfigure(index=1, weight=1)
        self.main_fr.rowconfigure(index=2, weight=1)

    def create_friend_frame(self):
        self.friend_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.friend_fr, text="Danh sách bạn bè", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        self.return_btn = tkinter.Button(self.friend_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def create_onl_user_frame(self):
        self.onl_user_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.onl_user_fr, text="Danh sách người dùng đang online", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        self.return_btn = tkinter.Button(self.onl_user_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def create_send_fr_request_frame(self):
        self.send_friend_request_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.send_friend_request_fr, text="Lời mời kết bạn đã gửi", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        self.return_btn = tkinter.Button(self.send_friend_request_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def create_fr_request_frame(self):
        self.friend_request_fr = tkinter.Frame()
        self.label = tkinter.Label(self.friend_request_fr, text="Lời mời kết bạn", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        self.return_btn = tkinter.Button(self.friend_request_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def show_friend(self):
        self.main_fr.grid_forget()

        self.current_fr = self.friend_fr
        self.friend_fr.grid(row=0, column=0)
   
    def show_onl_user(self):
        self.main_fr.grid_forget()

        self.current_fr = self.onl_user_fr
        self.onl_user_fr.grid(row=0, column=0)
    
    def show_fr_request(self):
        self.main_fr.grid_forget()

        self.current_fr = self.friend_request_fr
        self.friend_request_fr.grid(row=0, column=0)

    def show_send_fr_request(self):
        self.main_fr.grid_forget()

        self.current_fr = self.send_friend_request_fr
        self.send_friend_request_fr.grid(row=0, column=0)

    def show_main(self):
        self.current_fr.grid_forget()
        self.main_fr.grid(row=0, column=0)

    def log_out(self):
        self.main.destroy()

x = main_window()
x.start()