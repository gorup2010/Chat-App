import os
import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# Tạo tài khoản mới
def createNewAccount(username, password):
    # Kiểm tra tài khoản đã tạo chưa
    # PATH_TO_FILE: đường dẫn đến file
    PATH_TO_FILE = f'Account\{username}'
    if not os.path.exists(PATH_TO_FILE):
        newAcc = open(PATH_TO_FILE, 'w')
        newAcc.write(password)
        print("CREATE NEW FILE SUCCESS!")
    else:
        print("ERROR: ACCCOUNT IS EXIST!")


# Kiểm tra username và password
def validationAccount(username, password):
    PATH_TO_FILE = f'Account\{username}'
    # Kiểm tra xem username có tồn tại chưa
    if os.path.exists(PATH_TO_FILE):
        file = open(PATH_TO_FILE, 'r')
        passwordInFile = file.readline()
        # Kiểm tra xem password có đúng không
        if password == passwordInFile:
            print("LOGIN SUCCEED!")
        else:
            print("INVALID PASSWORD!")
    else:
        print("USERNAME CANNOT FOUND!")


# Bắt đầu đợi connection từ client
def start():
    server.listen()
    print("SERVER IS LISTINING!")
    while True:
        conn, addr = server.accept()
        # Tạo một thread mới để xử lí connection của client
        thread = threading.Thread(handleClient, (conn, addr))
        thread.start()


# Hàm dùng để thao tác với từng client
def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # Đợi nhận msg từ client
        msg = conn.recv(1024).decode(FORMAT)
        # Nếu client gửi yêu cầu DISCONNECT, thoát vòng lặp và server sẽ đóng socket
        if msg == DISCONNECT_MESSAGE:
            connected = False

        # In ra msg của client và gửi msg thông báo nhận msg thành công cho client
        print(f"[{addr}] {msg}")
        conn.send("Msg received".encode(FORMAT))
    
    # Server đóng socket
    conn.close()

