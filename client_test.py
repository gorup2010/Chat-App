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
RETRIEVE_FR_REQUEST_MSG = "FRREQUEST"
RETRIEVE_SEND_FR_REQUEST_MSG = "SREREQUEST"
RETRIEVE_ADDRESS = "ADDR"
ADDFRIEND_MSG = "ADD"
ACCEPT_MSG = "ACCEPT"

# Message nhận được từ server
# ADDFRIEND_MSG = "ADD"
# ACCEPT_MSG = "ACCEPT"

# Message gửi cho client
CHAT_MSG = "CHAT"

# Main window sẽ chạy khi ta đăng nhập hay đăng ký thành công
class man_window:
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
        msg = ADDFRIEND_MSG + ":" + Client.username + ":" + other_username
        Client.conns_s.send(msg.encode('utf-8'))


class main_window:
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.title(f'Chào mừng trở lại {Client.username}')

        self.create_main_frame()
        self.create_friend_frame()
        self.create_onl_user_frame()
        self.create_fr_request_frame()
        self.create_send_fr_request_frame()

        self.current_fr = None

        self.main.protocol("WM_DELETE_WINDOW", self.log_out)

    # Bắt đầu hiện màn hình chat app
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

        for friend in Client.list_of_friend:
            pass

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
        self.friend_request_fr = tkinter.Frame(self.main)
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
        # Ngắt hết kết nối với các user khác

        # Gửi log out msg cho server
        msg = LOGOUT_MSG + ":"
        Client.conns_s.send(msg.encode('utf-8'))

        # Trở lại cửa sổ đăng nhập
        Client.log_out()
        self.main.destroy()
        Client.show_login()

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

    # Bắt đầu loop login window
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
            self.hide()
            Client.retrieve_info_user()
            Client.start()

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
            Client.start()
            
    # Khi ta đăng nhập hoặc đăng ký thành công, cửa sổ đăng nhập sẽ đóng và chuyển sang cửa sổ main_waindow
    def hide(self):
        self.login.withdraw()

    # Hàm sẽ hiện login window trở lại khi client logout
    def show(self):    
        self.login.deiconify()

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

    # Một số list của client
    list_of_friend = []                         # Danh sách bạn bè của client
    list_of_onl_user = []                       # Danh sách online user
    list_of_chat_room = []                      # Danh sách phòng chat
    list_of_fr_request = []                     # Danh sách lời mời kết bạn
    list_of_send_fr_request = []                # Danh sách lời mời kết bạn đã gửi  

    # Một số biến check điều kiện
    isLogin = False

    # Một số màn hình của client
    login_win = login_window()
    main_win = None

    def __init__(self):        
        Client.login_win.start()

    def __del__(self):
        print("Da dong client")

    def create_main():
        Client.main_win = main_window()
        Client.main_win.start()

    def show_login():
        Client.login_win.show()

    def start():
        Client.isLogin = True
        Client.retrieve_onl_user()
        Client.create_main()
        # Tạo thread listen msg từ server và từ client
        s_thread = threading.Thread(target=Client.listen_to_server)
        s_thread.start()
        c_thread = threading.Thread(target=Client.listen_to_client)
        c_thread.start()

    # Hàm gửi msg cho server lấy về ds bạn bè, lời mời kết bạn nhận được và đã gửi của user
    def retrieve_info_user():
        # Lấy về ds bạn bè
        msg = RETRIEVE_FR_MSG + ":"
        Client.conns_s.sendall(msg.encode("utf-8"))
        data = Client.conns_s.recv(1024)
        Client.list_of_friend = pickle.loads(data)

        # Lấy về lời mời kết bạn nhận được
        msg = RETRIEVE_FR_REQUEST_MSG + ":"
        Client.conns_s.sendall(msg.encode("utf-8"))
        data = Client.conns_s.recv(1024)
        Client.list_of_onl_user = pickle.loads(data)

        # Lấy về lời mời kết bạn đã gửi
        msg = RETRIEVE_SEND_FR_REQUEST_MSG + ":"
        Client.conns_s.sendall(msg.encode("utf-8"))
        data = Client.conns_s.recv(1024)
        Client.list_of_onl_user = pickle.loads(data)

    # Hàm gửi msg cho server lấy về ds các user đang online khác
    def retrieve_onl_user():
        msg = RETRIEVE_ONL_MSG + ":"
        Client.conns_s.sendall(msg.encode("utf-8"))
        data = Client.conns_s.recv(1024)
        Client.list_of_onl_user = pickle.loads(data)

    # Socket kết nối với server đợi nhận msg từ server
    def listen_to_server(self):
        while Client.isLogin:
            msg = Client.conns_s.recv(1024).decode("utf-8")
            command, content = msg.split(':', 1)

    # Listen socket bắt đầu đợi nhận message từ các client khác
    def listen_to_client(self):
        Client.listen_s.listen()
        while Client.isLogin:
            conn_s, address = Client.listen_s.accept()
            # Tạo một thread mới để xử lí connection
            thread = threading.Thread(target=self.handle_client, args=(conn_s, address))
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

    def log_out():
        Client.username = ""
        Client.isLogin = False
        Client.list_of_chat_room = []
        Client.list_of_friend = []
        Client.list_of_onl_user = []
        Client.list_of_fr_request = []
        Client.list_of_send_fr_request = []

client = Client()