import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext
from tkinter import ttk
import random
import pickle
from functools import partial

SERVER_PORT = 8080
SERVER_HOST = socket.gethostbyname(socket.gethostname())
LISTEN_PORT = 5050 + random.randint(1, 100)
HOST = socket.gethostbyname(socket.gethostname())

# Message gửi cho server
LOGOUT_MSG = "LOGOUT"
LOGIN_MSG = "LOGIN"
SIGNUP_MSG = "SIGNUP"
CLOSE_MSG = "CLOSE"
RETRIEVE_FR_MSG = "FRIEND"
RETRIEVE_ONL_MSG = "ONLINE"
ADDFRIEND_MSG = "ADD"
# Message 
CHAT_MSG = "CHAT"

# Main window sẽ chạy khi ta đăng nhập hay đăng ký thành công
class main_window:
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.title(f'Chào mừng trở lại {Client.username}')
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

    def show(self):
        self.main.mainloop()

    def reset(self):
    # Lấy danh sách bạn bè
        #Gửi yêu cầu lấy ds bạn bè
        msg = RETRIEVE_FR_MSG + ":" + Client.username
        Client.conns_s.send(msg.encode('utf-8'))
        # Nhận list ds bạn bè
        temp = Client.conns_s.recv(1024)
        Client.list_of_friend = pickle.loads(temp)

    # Lấy danh sách online user
        #Gửi yêu cầu lấy ds online user
        msg = RETRIEVE_ONL_MSG + ":"
        Client.conns_s.send(msg.encode('utf-8'))
        # Nhận list ds online user
        temp = Client.conns_s.recv(1024)
        Client.list_of_onl_user = pickle.loads(temp)

    # Hiển thị danh sách user online trên frame user online
        for widget in self.on_second_frame.winfo_children():
            widget.destroy()
        for i in range(len(Client.list_of_onl_user)):
            username = Client.list_of_onl_user[i]
            if (username != Client.username) and (not username in Client.list_of_friend):
                btn = tkinter.Button(self.on_second_frame, text=f"{username}", font=5, command=partial(self.add_friend, username))
                btn.grid(row=i, column=0, pady=10, padx=10)
    
    # Hiển thị danh sách bạn bè của user
        for widget in self.fr_second_frame.winfo_children():
            widget.destroy()
        for i in range(len(Client.list_of_friend)):
            fr_name = Client.list_of_friend[i]
            if fr_name in Client.list_of_onl_user: 
                btn = tkinter.Button(self.fr_second_frame, text=f"{fr_name}", font=5)
            else:
                btn = tkinter.Button(self.fr_second_frame, text=f"{fr_name}", font=5, state="disabled")
            btn.grid(row=i, column=0, pady=10, padx=10)

    def add_friend(self, other_username):
        # Gửi yêu cầu kết bạn với máy chủ
        # msg bao gồm username của user và người user muốn kết bạn
        msg = ADDFRIEND_MSG + ":" + other_username
        Client.conns_s.send(msg.encode('utf-8'))

    def log_out(self):
        # Ngắt hết kết nối với các user khác

        # Gửi log out msg cho server
        msg = LOGOUT_MSG + ":"
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

    def show(self):    
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
            self.hide()

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
            self.hide()

    # Khi ta đăng nhập hoặc đăng ký thành công, cửa sổ đăng nhập sẽ đóng và chuyển sang cửa sổ main_waindow
    def hide(self):
        self.login.withdraw()
        Client.main_win.show()

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

    # Danh sách bạn bè, ds online user, ds các phòng chat mà user đang tham gia
    list_of_friend = []
    list_of_onl_user = []
    list_of_chat_room = []

    # Danh sách các màn hình của user
    login_win = login_window()
    main_win = main_window()

    def __init__(self):        
        self.login_win.show()

    def __del__(self):
        print("Da dong client")

    # Listen socket bắt đầu đợi nhận message từ các client khác
    def listen_to_client(self):
        self.listen_s.listen()
        while True:
            conn_s, address = self.listen_s.accept()
            # Tạo một thread mới để xử lí connection
            thread = threading.Thread(target=self.handle, args=(conn_s, address))
            thread.start()
    
    # Hàm xử lí các message nhận về
    def handle_client(self, conn_s, address):
        while True:
            msg = conn_s.recv(1024).decode('utf-8')
            command, content = msg.split(':', 1)

    def handle_fr_request(self, request):
        other_user = request.split(':', 1)[1]

        # Tạo cửa sổ hiển thị yêu cầu kết bạn
        win = tkinter.Toplevel()
        win.title("Yêu cầu kết bạn")

        lbl = tkinter.Label(win, text=f"Bạn nhận được yêu cầu kết bạn từ {other_user}", font=5)
        lbl.pack(pady=5)

        accept = tkinter.Button(win, text="Chấp nhận", font=5)
        accept.grid(row=1, column=0, pady=5, padx=5)

        deny = tkinter.Button(win, text="Từ chối", font=5)
        deny.grid(row=1, column=1, pady=5, padx=5)

client = Client()