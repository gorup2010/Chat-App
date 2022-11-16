import tkinter
import threading
from tkinter import simpledialog
import tkinter.scrolledtext
import socket

SERVER_PORT = 8080
SERVER_HOST = None
LISTEN_PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())

listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_s.bind((HOST, LISTEN_PORT))

conn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_s.connect((SERVER_HOST, SERVER_PORT))

login = tkinter.Tk()
login.geometry()

msg = conn_s.recv(1024)
