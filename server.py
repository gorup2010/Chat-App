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
            if command == CLOSE_MSG:
                conn_s.send("SUCCEED".encode('utf-8'))
                conn_s.close()
                print("Da dong socket")
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
        return result

    # Kiểm tra username
    def validation_account(self, username):
        if not os.path.exists('user.json'):
            result = "FaIL"
        else:
            with open('user.json', 'r') as file:
                data = json.load(file)
            if username in data:
                result = "SUCCEED"
            else:
                result = "FAIL"
        return result

    def close_conn(self, conn):
        conn.close()
        return "SUCCEED"

server = Server()
server.start()