import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext
from tkinter import ttk
import random

SERVER_PORT = 8080
SERVER_HOST = socket.gethostbyname(socket.gethostname())
LISTEN_PORT = 5050 + random.randint(1, 100)
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
        self.main.geometry('900x500')

        # Tạo label
        self.lbl_friend = tkinter.Label(master=self.main, text="Bạn Bè", font=10)
        self.lbl_friend.grid(row=0, column=0, pady=5)

        self.lbl_onl_user = tkinter.Label(master=self.main, text="Online User", font=10)
        self.lbl_onl_user.grid(row=0, column=1, pady=5)

        # Tạo frame hiển thị danh sách bạn bè
        self.frm_friend = tkinter.Frame(master=self.main, borderwidth= 4, relief="groove")
        self.frm_friend.grid(row=1, column=0, sticky='nwes')

        # Tạo scrolled bar cho frame hiển thị danh sách bạn bè
        self.fr_canvas = tkinter.Canvas(self.frm_friend)
        self.fr_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.fr_scrollbar = ttk.Scrollbar(master=self.frm_friend, orient=tkinter.VERTICAL, command=self.fr_canvas.yview)
        self.fr_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.fr_canvas.configure(yscrollcommand=self.fr_scrollbar.set)
        self.fr_canvas.bind('<Configure>', lambda e: self.fr_canvas.configure(scrollregion = self.fr_canvas.bbox("all")))

        self.fr_second_frame = tkinter.Frame(self.fr_canvas)

        self.fr_canvas.create_window((0,0), window=self.fr_second_frame, anchor="nw")

        for thing in range(100):
	        tkinter.Button(self.fr_second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=10, padx=10)

        # Tạo frame hiển thị user online
        self.frm_onl_user = tkinter.Frame(master=self.main, borderwidth= 4, relief="groove")
        self.frm_onl_user.grid(row=1, column=1, sticky='nwes')

        # Tạo scrolled bar cho frame hiển thị user online
        self.on_canvas = tkinter.Canvas(self.frm_onl_user)
        self.on_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.on_scrollbar = ttk.Scrollbar(master=self.frm_onl_user, orient=tkinter.VERTICAL, command=self.on_canvas.yview)
        self.on_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.on_canvas.configure(yscrollcommand=self.on_scrollbar.set)
        self.on_canvas.bind('<Configure>', lambda e: self.on_canvas.configure(scrollregion = self.on_canvas.bbox("all")))

        self.on_second_frame = tkinter.Frame(self.on_canvas)

        self.on_canvas.create_window((0,0), window=self.on_second_frame, anchor="nw")

        for thing in range(100):
	        tkinter.Button(self.on_second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=10, padx=10)

        # Config 2 frame bạn bè và user online
        self.main.columnconfigure(index=0, weight=1)
        self.main.columnconfigure(index=1, weight=1)
        self.main.rowconfigure(index=1, weight=1)

        #Tạo button để reset danh sách bạn bè và user online
        self.btn_reset = tkinter.Button(master=self.main, width=10, text="Reset", font=10, command=self.reset)
        self.btn_reset.grid(row=2, column=0, pady = 10)

        #Tạo button đăng xuất
        self.btn_exit = tkinter.Button(master=self.main, width=10, text="Log Out", font=10, command=self.log_out)
        self.btn_exit.grid(row=2, column=1, pady = 10)

        self.main.protocol("WM_DELETE_WINDOW", self.log_out)

    def start(self):
        self.main.mainloop()

    def reset(self):
        pass

    def log_out(self):
        # Ngắt hết kết nối với các user khác

        # Gửi log out msg cho server
        msg = LOGOUT_MSG + ":" + Client.username
        Client.conns_s.send(msg.encode('utf-8'))

        # Đợi phản hồi từ server
        msg = Client.conns_s.recv(1024).decode('utf-8')
        if msg == "SUCCEED":
            # Trở lại cửa sổ đăng nhập
            Client.username = ""
            self.main.destroy()
            login = login_window()
            login.start()

# Cửa sổ đăng nhập, đăng ký
class login_window:
    def __init__(self):
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
        username = self.username_entry.get()
        msg = LOGIN_MSG + ":" + username
        Client.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = Client.conns_s.recv(1024).decode('utf-8')
        if (result == "FAIL"):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này không tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == "SUCCEED"):
            Client.username = username
            user_info = (username, HOST, LISTEN_PORT)
            
            self.close()

    def send_signup(self):
        # Gửi signup request cho server
        username = self.username_entry.get()
        msg = SIGNUP_MSG + ":" + username
        Client.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = Client.conns_s.recv(1024).decode('utf-8')
        if (result == "FAIL"):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này đã tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == "SUCCEED"):
            Client.username = username
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
        
class Client:
    # Socket để listen connection từ các client khác
    listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_s.bind((HOST, LISTEN_PORT))

    # Socket kết nối với server
    conns_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conns_s.connect((SERVER_HOST, SERVER_PORT))

    # Username của client (sẽ có khi đăng nhập thành công)
    username = ""

    def __init__(self):        
        self.login_win = login_window()
        self.login_win.start()

    def __del__(self):
        self.listen_s.close()
        print("Da dong client")

client = Client()