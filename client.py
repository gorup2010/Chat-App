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
RETRIEVE_ADDRESS = "RETRIADDR"
ADDFRIEND_MSG = "ADD"
ACCEPT_MSG = "ACCEPT"

# Message nhận được từ server
LOGIN_SUCCEED = "SUCCEED"
LOGIN_FAIL = "FAIL"
CLOSE_SUCCEDD = "SUCCEED"
LOGOUT_SUCCEED = "OUT_SUCCEED"
USER_ONLINE = "ON"
USER_OFFLINE = "OFF"
USER_ADDRESS = "ADDR"
# ADDFRIEND_MSG = "ADD"
# ACCEPT_MSG = "ACCEPT"

# Message gửi cho client
CHAT_MSG = "CHAT"
INIT_MSG = "INIT"
NAME_MSG = "NAME"
CLOSE_CONN_MSG = "CLOSEC"
CONN_CLOSED_MSG = "SUCCEED"

class chat_window:
    def __init__(self, main_win, connc_s, username = ""):
        self.main_win = main_win
        self.connc_s = connc_s
        self.username = username
        self.isClose = False

        # Tạo thread để nhận msg từ user bên kia
        threading.Thread(target=self.listen_msg).start()

        # Nếu chưa có username, lấy về username của user bên kia
        if self.username == "":
            msg = INIT_MSG + ":"
            self.connc_s.send(msg.encode('utf-8'))

        # Đợi để nhận được username
        while True:
            if self.username != "":
                break

        # Tạo cửa sổ chat window với user kia
        self.chat_win = tkinter.Toplevel(self.main_win.main)
        self.chat_win.title(f"{self.main_win.username} đang chat với {self.username}")

        self.text_area = tkinter.scrolledtext.ScrolledText(self.chat_win)
        self.text_area.config(font=('arial', 14), height=15, width=50)
        self.text_area.pack(padx=4, pady=4)
        self.text_area['state'] = 'disabled'

        self.msg_lbl = tkinter.Label(self.chat_win, font=5, text="Nhắn tin: ")
        self.msg_lbl.pack(padx=4, pady=4)

        self.input_area = tkinter.Text(self.chat_win, font=('arial', 14), height=2, width=50)
        self.input_area.pack(padx=4, pady=4)

        self.send_msg_btn = tkinter.Button(self.chat_win, text="Gửi", font=5, width=10, command=self.send_msg)
        self.send_msg_btn.pack(padx=4, pady=4)

        self.chat_win.protocol("WM_DELETE_WINDOW", self.hide)

        # Nếu chat win này là do user chủ động tạo connection thì sẽ hiện lên, nếu không sẽ ẩn
        if username == "":
            self.isShow = False
            self.chat_win.withdraw()
        else:
            self.isShow = True

    def start(self):
        self.chat_win.mainloop()

    def hide(self):
        self.isShow = False
        self.chat_win.withdraw()

    def show(self):
        self.isShow = True
        self.chat_win.deiconify()

    def send_msg(self):
        if not self.isClose:
            # Gửi msg và nội dung tin nhắn cho user kia
            content = self.input_area.get('1.0', 'end')
            msg = CHAT_MSG + ":" + content
            self.connc_s.send(msg.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

            # Load nội dung tin nhắn của mình lên text area
            self.text_area['state'] = 'normal'
            self.text_area.insert('end', f"{self.main_win.username}: {content}")
            self.text_area.yview('end')
            self.text_area['state'] = 'disabled'

    def listen_msg(self):
        while True:
            msg = self.connc_s.recv(1024).decode('utf-8')
            command, content = msg.split(":", 1)

            # Nếu user bên kia chưa biết username của mình, gửi username của mình cho họ
            if command == INIT_MSG:
                msg = NAME_MSG + ":" + self.main_win.username
                self.connc_s.send(msg.encode('utf-8'))
            
            # User bên kia gửi về username của họ cho mình
            if command == NAME_MSG:
                self.username = content

            if command == CHAT_MSG:
                self.receive_chat_msg(content)

            if command == CLOSE_CONN_MSG:
                self.close_conn()
                break

            if command == CONN_CLOSED_MSG:
                self.isClose = True
                break

    def receive_chat_msg(self, content):
        # Load nội dung tin nhắn lên text area
        self.text_area['state'] = 'normal'
        self.text_area.insert('end', f"{self.username}: {content}")
        self.text_area.yview('end')
        self.text_area['state'] = 'disabled'

        # Chuyển btn của friend thành màu đỏ nếu chat win đang ẩn
        if not self.isShow:
            for btn in self.main_win.list_btn_of_friend:
                if btn[0] == self.username:
                    btn[1].configure(fg = "red")
                    break

    def send_close_msg(self):
        msg = CLOSE_CONN_MSG + ":"
        self.connc_s.send(msg.encode('utf-8'))

        while True:
            if self.isClose:
                break

        self.connc_s.close()

        # Load thông báo user offline lên chat win
        self.text_area['state'] = 'normal'
        self.text_area.insert('end', f"{self.username} đã log out. Cuộc hội thoại kết thúc.")
        self.text_area.yview('end')
        self.text_area['state'] = 'disabled'

        self.chat_win.protocol("WM_DELETE_WINDOW", self.destroy_chat_win)

    def close_conn(self):
        msg = CONN_CLOSED_MSG + ":"
        self.connc_s.send(msg.encode('utf-8'))
        self.connc_s.close()
        self.isClose = True

    def destroy_chat_win(self):
        self.main_win.list_of_chat_win.remove(self)
        self.chat_win.destroy()

class main_window:
    def __init__(self, username, loginw):
        self.login_w = loginw
        self.username = username

        # Danh sách các phòng chat với các user khác mà user đang kết nối
        self.list_of_chat_win = []

        # Close port
        self.close_port = 6060 + random.randint(1, 100)

        # Một số biến check điều kiện
        self.isLogout = False
        self.isWaiting = False

        # Biến dùng để lấy về info user khi gửi msg get addr
        self.recvInfo = ""

        # Socket kết nối với server
        self.conns_s = loginw.conns_s

        # Lấy về thông tin của user
        self.retrieve_info_user()

        # Tạo thread mới để recv msg từ server
        threading.Thread(target=self.listen_to_server).start()

        # Tạo socket để listen các connection khác và tạo thread mới để listen
        self.listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_s.bind((HOST, LISTEN_PORT))
        threading.Thread(target=self.listen_to_client).start()

        # Tạo màn hình chat app
        self.main = tkinter.Toplevel(loginw.login)
        self.main.title(f'Chào mừng trở lại {username}')

        self.create_main_frame()
        self.create_friend_frame()
        self.create_onl_user_frame()
        self.create_fr_request_frame()
        self.create_send_fr_request_frame()

        self.current_fr = None

        self.main.protocol("WM_DELETE_WINDOW", self.log_out)

        # Tạo event và event handler tương ứng khi nhận được một yêu cầu kết nối từ một user khác
        self.new_connc_s = None
        self.main.bind("<<ListenConnection>>", self.accept_new_conn)

    def __del__(self):
        print("Da xoa main win")

    # Lấy về user online, bạn bè, lời mời kết bạn nhận được và đã gửi
    def retrieve_info_user(self):
        # Lấy về ds bạn bè
        msg = RETRIEVE_FR_MSG + ":"
        self.conns_s.send(msg.encode("utf-8"))
        data = self.conns_s.recv(1024)
        self.list_of_friend = pickle.loads(data)

        # Lấy về ds user online
        msg = RETRIEVE_ONL_MSG + ":"
        self.conns_s.send(msg.encode("utf-8"))
        data = self.conns_s.recv(1024)
        self.list_of_onl_user = pickle.loads(data)
        self.list_of_onl_user.remove(self.username)

        # Lấy về lời mời kết bạn nhận được
        msg = RETRIEVE_FR_REQUEST_MSG + ":"
        self.conns_s.send(msg.encode("utf-8"))
        data = self.conns_s.recv(1024)
        self.list_of_fr_request = pickle.loads(data)

        # Lấy về lời mời kết bạn đã gửi
        msg = RETRIEVE_SEND_FR_REQUEST_MSG + ":"
        self.conns_s.send(msg.encode("utf-8"))
        data = self.conns_s.recv(1024)
        self.list_of_send_fr_request = pickle.loads(data)

    # Thread để xử lí các msg nhận được từ server
    def listen_to_server(self):
        while True:
            msg = self.conns_s.recv(1024).decode("utf-8")
            command, content = msg.split(":", 1)

            if command == LOGOUT_SUCCEED:
                self.isLogout = True
                break

            if command == ADDFRIEND_MSG:
                self.add_fr_req(content)

            if command == ACCEPT_MSG:
                self.add_fr(content)

            if command == USER_ONLINE:
                self.add_onl_user(content)

            if command == USER_ADDRESS:
                self.recvInfo = content
                self.isWaiting = False

            if command == USER_OFFLINE:
                self.update_user_offline(content)

    # Thread để listen các connection khác
    def listen_to_client(self):
        self.listen_s.listen()
        while True:
            conn_s, address = self.listen_s.accept()
            if address == (HOST, self.close_port):
                conn_s.close()
                self.listen_s.close()
                break
            else:
                self.new_connc_s = conn_s
                self.main.event_generate("<<ListenConnection>>", when='tail')

    def accept_new_conn(self, event):
        # Tạo một chat win mới khi nhận được yêu cầu kết nối từ người khác
        new_chat_win = chat_window(self, self.new_connc_s)
        self.list_of_chat_win.append(new_chat_win)
        self.new_connc_s = None
        new_chat_win.start()

    # Đăng xuất
    def log_out(self):
        # Gửi log out msg cho server
        msg = LOGOUT_MSG + ":"
        self.conns_s.send(msg.encode('utf-8'))

        # Đợi phản hồi từ server
        while True: 
            if self.isLogout:
                break

        # Đợi cho mọi chat win đều đã close
        for chat_win in self.list_of_chat_win:
            while not chat_win.isClose:
                pass

        # Tạo một thread tạm để connect với listen port của client và giúp đóng nó
        close_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_s.bind((HOST, self.close_port))
        close_s.connect((HOST, LISTEN_PORT))
        close_s.close()

        # Xóa main window
        self.main.destroy()
        self.login_w.show()

    def update_user_offline(self, username):
        # Kiểm tra xem đó có phải user online hay là bạn bè của mình, nếu là user onl thì sẽ xóa btn user onl
        for btn in self.list_btn_of_onl_user:
            if btn[0] == username:
                btn[1].destroy()
                self.list_btn_of_onl_user.remove(btn)
                return

        # Nếu là bạn bè của mình thì disable btn friend
        for btn in self.list_btn_of_friend:
            if btn[0] == username:
                btn[1]['state'] = 'disabled'
                btn[1].configure(disabledforeground="gray")

        # Kiểm tra xem có đang connect vs user vừa offline không
        for chat_win in self.list_of_chat_win:
            if chat_win.username == username:
                chat_win.send_close_msg()
        
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

    # Implement danh sách bạn bè và các chức năng liên quan tới nó
    def create_friend_frame(self):
        self.friend_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.friend_fr, text="Danh sách bạn bè", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        # Tạo scrolled bar cho frame hiển thị danh sách bạn bè
        self.friend_container = tkinter.Frame(self.friend_fr)
        self.friend_container.pack()

        self.fr_canvas = tkinter.Canvas(self.friend_container)
        self.fr_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.fr_scrollbar = ttk.Scrollbar(master=self.friend_container, orient=tkinter.VERTICAL, command=self.fr_canvas.yview)
        self.fr_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.fr_canvas.configure(yscrollcommand=self.fr_scrollbar.set)
        self.fr_canvas.bind('<Configure>', lambda e: self.fr_canvas.configure(scrollregion = self.fr_canvas.bbox("all")))

        self.fr_second_frame = tkinter.Frame(self.fr_canvas)

        self.fr_canvas.create_window((0,0), window=self.fr_second_frame, anchor="nw")

        # Tạo list những button bạn bè của user
        self.list_btn_of_friend = []
        i = 0
        for friend in self.list_of_friend:
            btn = tkinter.Button(self.fr_second_frame, fg="green", text=friend, font=4, width=36, command=partial(self.open_chat_win,friend))
            if not friend in self.list_of_onl_user:
                btn['state'] = 'disabled'
                btn.configure(disabledforeground="gray")
            btn.grid(row=i, column=0, sticky="ew")
            self.list_btn_of_friend.append([friend, btn])
            i += 1

        self.return_btn = tkinter.Button(self.friend_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def open_chat_win(self, username):
        # Tìm xem đã có chat room với username chưa
        for chat_win in self.list_of_chat_win:
            if chat_win.username == username and not chat_win.isClose:
                # Nếu chat win bị ẩn đi thì sẽ mở nó lên
                if not chat_win.isShow:
                    chat_win.show()
                    for btn in self.list_btn_of_friend:
                        if btn[0] == username:
                            btn[1].configure(fg="green")
                return

        # Nếu chưa có chat room với username thì gửi msg lấy về address của username trên server
        msg = RETRIEVE_ADDRESS + ":" + username
        self.conns_s.send(msg.encode("utf-8"))

        self.isWaiting = True
        while True:
            if not self.isWaiting:
                break
        self.create_new_chat_win(self.recvInfo)
        self.recvInfo = ""

    def create_new_chat_win(self, info):
        # Chủ động tạo connection với user khác
        username, host, lport = info.split(':', 2)

        # Tạo socket kết nối với user kia
        connc_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connc_s.connect((host, int(lport)))

        # Tạo một chat win mới với user kia
        new_chat_win = chat_window(self, connc_s, username)
        self.list_of_chat_win.append(new_chat_win)
        new_chat_win.start()

    def add_fr(self, username):
        self.list_of_friend.append(username)

        # Thêm một btn mới với username vào friend frame
        btn = tkinter.Button(self.fr_second_frame, fg="green", text=username, font=4, width=36, command=partial(self.open_chat_win,username))
        btn.grid(row=len(self.list_of_friend) - 1, column=0, sticky="ew")
        self.list_btn_of_friend.append([username, btn])

        # Xóa đi btn với username ở bên onl user
        self.list_of_onl_user.remove(username)
        for btn in self.list_btn_of_onl_user:
            if btn[0] == username:
                btn[1].destroy()
                self.list_btn_of_onl_user.remove(btn)
                break

        # Xóa đi send fr req đã gửi cho người vừa accept mình
        self.list_of_send_fr_request.remove(username)
        for btn in self.list_btn_of_send_friend_request_fr:
            if btn[0] == username:
                btn[1].destroy()
                self.list_btn_of_send_friend_request_fr.remove(btn)
                break

    # Implement danh sách useronline và các chức năng liên quan tới nó
    def create_onl_user_frame(self):
        self.onl_user_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.onl_user_fr, text="Danh sách người dùng đang online", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        # Tạo scrolled bar cho frame hiển thị onl user
        self.container = tkinter.Frame(self.onl_user_fr)
        self.container.pack()

        self.canvas = tkinter.Canvas(self.container)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(master=self.container, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.onl_second_frame = tkinter.Frame(self.canvas)

        self.canvas.create_window((0,0), window=self.onl_second_frame, anchor="nw")

        # Tạo list những button user đang online
        self.list_btn_of_onl_user = []
        i = 0
        for onuser in self.list_of_onl_user:
            if not onuser in self.list_of_friend:
                btn = tkinter.Button(self.onl_second_frame, fg="black", text=onuser, font=4, width=36, command=partial(self.send_add_fr, onuser))
                if onuser in self.list_of_send_fr_request:
                    btn['state'] = 'disabled'
                    btn.configure(disabledforeground="gray")
                btn.grid(row=i, column=0, sticky="ew")
                self.list_btn_of_onl_user.append([onuser, btn])
                i += 1
            else:
                self.list_of_onl_user.remove(onuser)        

        self.return_btn = tkinter.Button(self.onl_user_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def send_add_fr(self, username):
        msg = ADDFRIEND_MSG + ":" + username
        self.conns_s.send(msg.encode("utf-8"))
        
        self.list_of_send_fr_request.append(username)

        # Thêm vào list send req button một req mới
        btn = tkinter.Button(self.sreq_second_frame, fg="black", text=username, font=4, width=36)
        btn.grid(row=len(self.list_of_send_fr_request) - 1, column=0, sticky="ew")
        self.list_btn_of_send_friend_request_fr.append([username, btn])

        # Disable button của onl user vừa mới gửi lời mời kết bạn để không gửi nữa
        for btn in self.list_btn_of_onl_user:
            if btn[0] == username:
                btn[1]['state'] = 'disabled'
                btn[1].configure(disabledforeground="gray")
                break

    def add_onl_user(self, username):
        # Nếu user vừa online là bạn mình chỉ cần chỉnh button của họ ở friend fr bình thường lại là được
        for friend in self.list_btn_of_friend:
            if friend[0] == username:
                friend[1]['state'] = 'normal'
                return

        # Nếu user vừa online không phải bạn mình
        self.list_of_onl_user.append(username)
        btn = tkinter.Button(self.onl_second_frame, fg="black", text=username, font=4, width=36, command=partial(self.send_add_fr,username))
        btn.grid(row=len(self.list_of_onl_user) - 1, column=0, sticky="ew")
        self.list_btn_of_onl_user.append([username, btn])

    # Implement danh sách lời mời kết bạn đã gửi và các chức năng liên quan tới nó
    def create_send_fr_request_frame(self):
        self.send_friend_request_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.send_friend_request_fr, text="Lời mời kết bạn đã gửi", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        # Tạo scrolled bar cho frame hiển thị send friend request
        self.container = tkinter.Frame(self.send_friend_request_fr)
        self.container.pack()

        self.canvas = tkinter.Canvas(self.container)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(master=self.container, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.sreq_second_frame = tkinter.Frame(self.canvas)

        self.canvas.create_window((0,0), window=self.sreq_second_frame, anchor="nw")

        # Tạo list những button danh sách các lời mời kết bạn đã gửi
        self.list_btn_of_send_friend_request_fr = []
        i = 0
        for sreq in self.list_of_send_fr_request:
            btn = tkinter.Button(self.sreq_second_frame, fg="black", text=sreq, font=4, width=36)
            btn.grid(row=i, column=0, sticky="ew")
            self.list_btn_of_send_friend_request_fr.append([sreq, btn])
            i += 1

        self.return_btn = tkinter.Button(self.send_friend_request_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    # Implement danh sách lời mời kết bạn và các chức năng liên quan tới nó
    def create_fr_request_frame(self):
        self.friend_request_fr = tkinter.Frame(self.main)
        self.label = tkinter.Label(self.friend_request_fr, text="Lời mời kết bạn", font=6, width=40)
        self.label.pack(padx=4,pady=4)

        # Tạo scrolled bar cho frame hiển thị friend request
        self.container = tkinter.Frame(self.friend_request_fr)
        self.container.pack()

        self.canvas = tkinter.Canvas(self.container)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(master=self.container, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.req_second_frame = tkinter.Frame(self.canvas)

        self.canvas.create_window((0,0), window=self.req_second_frame, anchor="nw")

        # Tạo list những button danh sách các lời mời kết bạn
        self.list_btn_of_fr_request = []
        i = 0
        for req in self.list_of_fr_request:
            btn = tkinter.Button(self.req_second_frame, fg="black", text=req, font=4, width=36, command=partial(self.accept,req))
            btn.grid(row=i, column=0, sticky="ew")
            self.list_btn_of_fr_request.append([req, btn])
            i += 1

        self.return_btn = tkinter.Button(self.friend_request_fr, text="Quay lại", command=self.show_main, font=6)
        self.return_btn.pack(padx=4,pady=4)

    def accept(self, username):
        msg = ACCEPT_MSG + ":" + username
        self.conns_s.send(msg.encode("utf-8"))

        self.list_of_friend.append(username)

        # Thêm một btn mới với username vào friend frame
        btn = tkinter.Button(self.fr_second_frame, fg="green", text=username, font=4, width=36, command=partial(self.open_chat_win,username))
        btn.grid(row=len(self.list_of_friend) - 1, column=0, sticky="ew")
        self.list_btn_of_friend.append([username, btn])

        # Xóa đi btn với username ở bên onl user
        self.list_of_onl_user.remove(username)
        for btn in self.list_btn_of_onl_user:
            if btn[0] == username:
                btn[1].destroy()
                self.list_btn_of_onl_user.remove(btn)
                break

        # Xóa đi btn với username ở fr request
        self.list_of_fr_request.remove(username)
        for btn in self.list_btn_of_fr_request:
            if btn[0] == username:
                btn[1].destroy()
                self.list_btn_of_fr_request.remove(btn)
                break

    def add_fr_req(self, username):
        # Thêm vào fr req frame một button mới
        self.list_of_fr_request.append(username)

        btn = tkinter.Button(self.req_second_frame, fg="black", text=username, font=4, width=36, command=partial(self.accept,username))
        btn.grid(row=len(self.list_of_fr_request) - 1, column=0, sticky="ew")
        self.list_btn_of_fr_request.append([username, btn])

        # Set btn của fr req bên onl user thành disable
        for btn in self.list_btn_of_onl_user:
            if btn[0] == username:
                btn[1]['state'] = 'disabled'
                btn[1].configure(disabledforeground="gray")

    # Hàm show ở dưới là để bật tắt các frame tương ứng khi nhấn vào các button trên màn hình
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

# Cửa sổ đăng nhập, đăng ký
class login_window:
    def __init__(self):
        # Socket kết nối với server
        self.conns_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conns_s.connect((SERVER_HOST, SERVER_PORT))

        # Tạo màn hình đăng nhập
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
        msg = LOGIN_MSG + ":" + username + ":" + str(LISTEN_PORT)
        self.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = self.conns_s.recv(1024).decode('utf-8')
        if (result == LOGIN_FAIL):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này không tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == LOGIN_SUCCEED):
            self.hide()
            self.start_new_mainwin(username)    

    def send_signup(self):
        # Gửi signup request cho server
        username = self.username_entry.get()
        msg = SIGNUP_MSG + ":" + username + ":" + str(LISTEN_PORT)
        self.conns_s.send(msg.encode('utf-8'))
        self.username_entry.delete('0', 'end')

        # Kiểm tra kết quả
        result = self.conns_s.recv(1024).decode('utf-8')
        if (result == LOGIN_FAIL):
            fail_window = tkinter.Toplevel()
            fail_window.title("Thất bại")
            fail_txt = tkinter.Label(master=fail_window, text="Tài khoản này đã tồn tại", font=10)
            fail_txt.pack(padx=4, pady=4)
            fail_window.mainloop()
        if (result == LOGIN_SUCCEED):
            self.hide()
            self.start_new_mainwin(username)

    # Tạo một màn hình ứng dụng mới cho client đã đăng nhập thành công
    def start_new_mainwin(self, username):
        # Tạo main win và bắt đầu vào main loop
        self.main_window = main_window(username, self)
        self.main_window.start()

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
        self.conns_s.send(msg.encode('utf-8'))

        # Chờ phản hồi từ server
        msg = self.conns_s.recv(1024).decode('utf-8')
        if msg == CLOSE_SUCCEDD:
            self.conns_s.close()
            self.login.destroy()

login = login_window()
login.start()