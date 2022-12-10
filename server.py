import os
import socket
import threading
import json
import pickle

# Địa chỉ của server
PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())

# Message nhận được từ user
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

# Message server gửi cho user
# ADDFRIEND_MSG = "ADD"
# ACCEPT_MSG = "ACCEPT"

class Server:
    def __init__(self):
        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_s.bind((HOST, PORT))

        # Dictionary theo dõi các user đang online
        # { 'username' : {
        #       'address' : (host user, listen port user) }
        #       'conn' : conn_s 
        self.onl_dict = {}

    # Server sẽ bắt đầu nhận yêu cầu kết nối từ client và thực hiện kết nối
    def start(self):
        self.server_s.listen()
        print("Server start")
        while True:
            conn_s, address = self.server_s.accept()
            print(f"Connect with {str(address)}")
            # Tạo một thread mới để chạy connection với client
            thread = threading.Thread(target=self.handle, args=(conn_s, address))
            thread.start()

    def handle(self, conn_s, address):
        print(f"New thread create to handle {str(address)}")
        # Username của client mà thread này đang xử lí
        username = ""

        while True:
            msg = conn_s.recv(1024).decode('utf-8')
            if msg != "":
                print(f"Nhan duoc msg: {msg}")
            command, content = msg.split(':', 1)

            result = ""
            if command == SIGNUP_MSG:
                result, username = self.create_new_account(content, conn_s, address)

            if command == LOGIN_MSG:
                result, username = self.validation_account(content, conn_s, address)

            if command == LOGOUT_MSG:
                result = self.log_out(username)
                username = ""

            if command == RETRIEVE_FR_MSG:
                list_of_fr = self.retrieve_fr(username)
                conn_s.sendall(pickle.dumps(list_of_fr))

            if command == RETRIEVE_FR_REQUEST_MSG:
                list_of_fr_request = self.retrieve_fr_request(username)
                conn_s.sendall(pickle.dumps(list_of_fr_request))

            if command == RETRIEVE_SEND_FR_REQUEST_MSG:
                list_of_send_fr_request = self.retrieve_send_fr_request(username)
                conn_s.sendall(pickle.dumps(list_of_send_fr_request))

            if command == RETRIEVE_ONL_MSG:
                list_of_onl_user = self.retrieve_onl_user()
                conn_s.sendall(pickle.dumps(list_of_onl_user))

            if command == ADDFRIEND_MSG:
                self.send_fr_request(username, content)

            if command == ACCEPT_MSG:
                self.accept_fr_request(username, content)

            if command == CLOSE_MSG:    # Client yêu cầu ngắt kết nối
                # Gửi phản hồi về cho client và đóng socket
                conn_s.send("SUCCEED".encode('utf-8'))
                conn_s.close()
                print(f"Connection with {str(address)} close")
                break

            if result != "":
                conn_s.send(result.encode('utf-8'))

    # Tạo tài khoản mới
    def create_new_account(self, username, conn_s, address):
        if not os.path.exists('user.json'):
            # Thêm tài khoản vào file user.json
            data = {
                username: {
                    "status" : True,
                    "friend" : [],
                    "fr_request" : [],
                    "send_fr_request" : []
                }
            }
            with open('user.json', 'w') as file:
                json.dump(data, file, indent=2)
            result = "SUCCEED"
            username_res = username
            # Thêm user vào dict on_user
            self.onl_dict[username] = {
                "address" : address,
                "conn" : conn_s
            }

            print(f"New account: {username}")     
        else:
            with open('user.json', 'r') as file:
                data = json.load(file)
            if username in data:
                result = "FAIL"
                username_res = ""
            else:
                # Thêm tài khoản vào file user.json
                data[username] = {
                    "status" : True,
                    "friend" : [],
                    "fr_request" : [],
                    "send_fr_request" : []
                }
                with open('user.json', 'w') as file:
                    json.dump(data, file, indent=2)
                result = "SUCCEED"
                username_res = username

                # Thêm user vào dict on_user
                self.onl_dict[username] = {
                    "address" : address,
                    "conn" : conn_s
                }

                print(f"New account: {username}") 
        return result, username_res

    # Kiểm tra username
    def validation_account(self, username, conn_s, address):
        if not os.path.exists('user.json'):
            result = "FAIL"
            username_res = ""
        else:
            with open('user.json', 'r') as file:
                data = json.load(file)
            if username in data:
                # Chỉnh sửa trạng thái của user thành online
                data[username]["status"] = True
                with open('user.json', 'w') as file:
                    json.dump(data, file, indent=2)
                result = "SUCCEED"
                username_res = username
                print(f"{username} log in")  

                # Thêm user vào dict on_user
                self.onl_dict[username] = {
                    "address" : address,
                    "conn" : conn_s
                }
            else:
                result = "FAIL"
                username_res = ""
        return result, username_res

    # Username yêu cầu đăng xuất
    def log_out(self, username):
        # Thông báo cho mọi user khác user này đã offline
        # msg = 
        # for user in self.onl_dict:
        #     user['conn'].send

        # Xóa user trong onl user list
        del self.onl_dict[username]
 
        # Chỉnh sửa trạng thái của user thành offline
        with open('user.json', 'r') as file:
                data = json.load(file)
        data[username]["status"] = False
        with open('user.json', 'w') as file:
            json.dump(data, file, indent=2)
        print(f"{username} log out")
        return "SUCCEED"

    # Lấy danh sách bạn bè của user
    def retrieve_fr(self, username):
        with open('user.json', 'r') as file:
            data = json.load(file)
        res = data[username]["friend"]
        return res

    # Lấy danh sách lời mời kết bạn của user
    def retrieve_fr_request(self, username):
        with open('user.json', 'r') as file:
            data = json.load(file)
        res = data[username]["fr_request"]
        return res

    # Lấy danh sách lời mời kết bạn đã gửi của user
    def retrieve_send_fr_request(self, username):
        with open('user.json', 'r') as file:
            data = json.load(file)
        res = data[username]["send_fr_request"]
        return res

    # Lấy danh sách user online
    def retrieve_onl_user(self):
        return list(self.onl_dict)

    # Gửi lời mời kết bạn của một user này cho một user khác
    # send user là người gửi lời mời kết bạn, recv user là người nhận lời mời kết bạn
    def send_fr_request(self, send_user, recv_user):
        with open('user.json', 'r') as file:
            data = json.load(file)

        # Thêm vào send user một send_fr_request mới và recv user một fr_request mới
        data[send_user]['send_fr_request'].append(recv_user)
        data[recv_user]['fr_request'].append(send_user)
        with open('user.json', 'w') as file:
            json.dump(data, file)

        # Gửi lời mời kết bạn của send user cho recv user
        if recv_user in self.onl_dict:
            msg = ADDFRIEND_MSG + ':' + send_user
            self.onl_dict[recv_user]['conn'].send(msg.encode('utf-8'))

    # User chấp nhận lời mời kết bạn từ user khác
    # send_user là người chấp nhân, recv_user là người được chấp nhận
    def accept_fr_request(self, send_user, recv_user):
        with open('user.json', 'r') as file:
            data = json.load(file)

        # Thêm 2 user vào danh sách bạn bè của nhau
        data[send_user]['friend'].append(recv_user)
        data[recv_user]['friend'].append(send_user)

        # Xóa đi fr_request của send user và send_fr_request của recv user
        data[send_user]['fr_request'].remove(recv_user)
        data[recv_user]['send_fr_request'].remove(send_user)

        with open('user.json', 'w') as file:
            json.dump(data, file)        
        
        # Gửi thông báo chấp nhận lời mời kết bạn của send user cho recv user
        if recv_user in self.onl_dict:
            msg = ACCEPT_MSG + ':' + send_user
            self.onl_dict[recv_user]['conn'].send(msg.encode('utf-8'))


server = Server()
server.start()