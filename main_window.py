import socket
import threading
import tkinter
from tkinter import simpledialog
import tkinter.scrolledtext
from tkinter import ttk
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

        # for thing in range(100):
	    #   tkinter.Button(self.fr_second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=10, padx=10)

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

        # for thing in range(100):
	    #     tkinter.Button(self.on_second_frame, text=f'Button {thing} Yo!').grid(row=thing, column=0, pady=4, padx=4)

        # Config 2 frame bạn bè và user online
        self.main.columnconfigure(index=0, weight=1)
        self.main.columnconfigure(index=1, weight=1)
        self.main.rowconfigure(index=1, weight=1)

        #Tạo button để reset danh sách bạn bè và user online
        self.btn_reset = tkinter.Button(master=self.main, width=10, text="Reset", font=10)
        self.btn_reset.grid(row=2, column=0, columnspan=2, pady = 10)
    
    def start(self):
        self.main.mainloop()

    def close(self):
        pass

x = main_window()
x.start()