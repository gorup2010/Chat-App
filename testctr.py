import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext

SERVER_PORT = 8080
SERVER_HOST = socket.gethostbyname(socket.gethostname())
LISTEN_PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())

LOGOUT_MSG = "LOGOUT"
LOGIN_MSG = "LOGIN"
SIGNUP_MSG = "SIGNUP"
CLOSE_MSG = "CLOSE"

# Main window sẽ chạy khi ta đăng nhập hay đăng ký thành công
class main_window:
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.title('Chat Application')

        self.frm_friend = tkinter.Frame(master=self.main, height=200, width=200, bg='blue')
        self.frm_friend.pack(side=tkinter.LEFT)

        self.frm_onl_user = tkinter.Frame(master=self.main, height=200, width=200, bg='red')
        self.frm_onl_user.pack(side=tkinter.LEFT)

    def start(self):
        self.main.mainloop()

    def close(self):
        pass

# Cửa sổ đăng nhập, đăng ký
class login_window:
    def __init__(self, conns_s):
        # Socket nối client với server
        self.conns_s = conns_s

        # Màn hình đăng nhập
        self.login = tkinter.Tk()
        self.login.title('Đăng nhập')
        self.login.geometry('250x200')

        self.label = tkinter.Label(master=self.login ,text='Tên người dùng', font=20)
        self.label.pack(pady=15)

        self.username_entry = tkinter.Entry(master=self.login ,background='white', width=20, font=17)
        self.username_entry.pack(pady=15)

        self.frm_button = tkinter.Frame(master=self.login)
        self.frm_button.pack(pady=10)

        self.btn_login = tkinter.Button(master=self.frm_button, text='Đăng nhập', width=10, command=self.send_login)
        self.btn_login.grid(column=1,row=1, padx=10)

        self.btn_signup = tkinter.Button(master=self.frm_button, text='Đăng kí', width=10, command=self.send_signup)
        self.btn_signup.grid(column=2,row=1, padx=10)

        self.login.protocol("WM_DELETE_WINDOW", self.direct_close_win)

    def start(self):    
        self.login.mainloop()

    def send_login(self):
        # Gửi login request cho server
        msg = LOGIN_MSG + ":" + self.username_entry.get()
        Client.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = Client.conns_s.recv(1024).decode('utf-8')
        print(result)
        if (result == "FAIL"):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này không tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == "SUCCEED"):
            self.close()

    def send_signup(self):
        # Gửi signup request cho server
        msg = SIGNUP_MSG + ":" + self.username_entry.get()
        Client.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = Client.conns_s.recv(1024).decode('utf-8')
        print(result)
        if (result == "FAIL"):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này đã tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == "SUCCEED"):
            self.close()

    # Khi ta đăng nhập hoặc đăng ký thành công, cửa sổ đăng nhập sẽ đóng và chuyển sang cửa sổ main_waindow
    def close(self):
        self.login.destroy()
        new_window = main_window()
        new_window.start()

    # Hàm sẽ chạy khi nhấn nút X để đóng cửa sổ đăng nhập
    def direct_close_win(self):
        # Gửi CLOSE_MSG cho server
        msg = CLOSE_MSG + ":"
        Client.conns_s.send(msg.encode('utf-8'))

        # Chờ phản hồi từ server
        msg = Client.conns_s.recv(1024).decode('utf-8')
        if msg == "SUCCEED":
            Client.conns_s.close()
            Client.listen_s.close()
            self.login.destroy()
            print("Da dong thanh cong")
        
class Client:
    # Socket để listen connection từ các client khác
    listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_s.bind((HOST, LISTEN_PORT))

    # Socket kết nối với server
    conns_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conns_s.connect((SERVER_HOST, SERVER_PORT))

    def __init__(self):        
        self.login_win = login_window(self.conns_s)
        self.login_win.start()

    def __del__(self):
        self.listen_s.close()
        print("Da dong client")

client = Client()