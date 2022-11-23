import os
import socket
import threading
import json
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext

PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())

LOGOUT_MSG = "LOGOUT"
LOGIN_MSG = "LOGIN"
SIGNUP_MSG = "SIGNUP"
CLOSE_MSG = "CLOSE"

class Server:
    def __init__(self):
        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_s.bind((HOST, PORT))
        # List theo dõi các user đang online
        self.onl_li = []
    
    def __del__(self):
        self.server_s.close()
        print("Da dong server")

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
        while True:
            msg = conn_s.recv(1024).decode('utf-8')
            if msg != "":
                print(f"Nhan duoc msg: {msg}")
            command, content = msg.split(':', 1)

            result = ""
            if command == SIGNUP_MSG:
                result = self.create_new_account(content)
            if command == LOGIN_MSG:
                result = self.validation_account(content)
            if command == LOGOUT_MSG:
                result = self.log_out(content)
            if command == CLOSE_MSG:    # Client yêu cầu ngắt kết nối
                # Gửi phản hồi về cho client và đóng socket
                conn_s.send("SUCCEED".encode('utf-8'))
                conn_s.close()
                print(f"Connection with {str(address)} close")
                break
            if result != "":
                conn_s.send(result.encode('utf-8'))

    # Tạo tài khoản mới
    def create_new_account(self, username):
        if not os.path.exists('user.json'):
            data = {
                username: {
                    "status" : True,
                    "friend" : []
                }
            }
            with open('user.json', 'w') as file:
                json.dump(data, file, indent=2)
            result = "SUCCEED"
            print(f"New account: {username}")       
        else:
            with open('user.json', 'r') as file:
                data = json.load(file)
            if username in data:
                result = "FAIL"
            else:
                data[username] = {
                    "status" : True,
                    "friend" : []
                }
                with open('user.json', 'w') as file:
                    json.dump(data, file, indent=2)
                result = "SUCCEED"
                print(f"New account: {username}")  
        return result

    # Kiểm tra username
    def validation_account(self, username):
        if not os.path.exists('user.json'):
            result = "FAIL"
        else:
            with open('user.json', 'r') as file:
                data = json.load(file)
            if username in data:
                # Chỉnh sửa trạng thái của user thành online
                data[username]["status"] = True
                with open('user.json', 'w') as file:
                    json.dump(data, file, indent=2)
                
                result = "SUCCEED"
                print(f"{username} log in")  
            else:
                result = "FAIL"
        return result

    # Username yêu cầu đăng xuất
    def log_out(self, username):
        # Xóa user trong onl user list
        self.onl_li.remove(username)

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



server = Server()
server.start()