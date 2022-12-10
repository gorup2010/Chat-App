import tkinter
import threading
from functools import partial
import random
import tkinter.scrolledtext

# class meme:
#     x = 0

#     def __init__(self) -> None:
#         self.win = tkinter.Tk()

#         self.frm = tkinter.Frame(self.win)
#         self.frm.pack()

#         for i in range(10):
#             self.lbl = tkinter.Label(self.frm, text=f"{i}")
#             self.lbl.pack()

#         self.lbl = tkinter.Button(self.win, text="Hi am jack", command=partial(self.foo))
#         self.lbl.pack()

#     # def foo(self, str):
#     #     if self.lbl['state'] == 'normal':
#     #         self.lbl["state"] = "disabled"
#     #         self.lbl.configure(disabledforeground='black')
#     #     ano = tkinter.Toplevel()
#     #     ano.title(str)
#     #     ano.mainloop()
    
#     def foo(self):
#         for thing in self.frm.winfo_children():
#             thing.destroy()

#         if (self.x % 2 == 0):
#             for i in range(20):
#                 self.lbl = tkinter.Label(self.frm, text=f"{10 - i}")
#                 self.lbl.pack()
#         else:
#             for i in range(5):
#                 self.lbl = tkinter.Label(self.frm, text=f"{100 - i}")
#                 self.lbl.pack()

#         self.x += 1


#     def start(self):
#         self.win.mainloop()

# x = meme()
# x.start()

# win = tkinter.Tk()
# win.title("Yêu cầu kết bạn")

# lbl = tkinter.Label(win, text=f"Bạn nhận được yêu cầu kết bạn từ ", font=5)
# lbl.grid(row=0, column=0, columnspan=2, pady=5, padx=5)

# def foo(btn: tkinter.Button):
#     btn.configure(text=f"{random.randint(1,100)}")

# accept = tkinter.Button(win, text="Chấp nhận", font=5)
# accept.grid(row=1, column=0, pady=5, padx=5)
# accept.configure(command=partial(foo, accept))

# def meme(str):
#     print(str)

# deny = tkinter.Button(win, text="Từ chối", font=5, command=lambda: meme(18))
# deny.grid(row=1, column=1, pady=5, padx=5)

# win.mainloop()

#Bật tắt hiện frame
win = tkinter.Tk()

i = True

lblx = tkinter.scrolledtext.ScrolledText(win, width=30, height=15)
lblx.grid(row=0,column=0,pady=5)

lbly = tkinter.scrolledtext.ScrolledText(win, width=30, height=15)
lbly.grid(row=0,column=0,pady=5)
lbly.grid_forget()

def foo():
    global i
    if i:
        lblx.grid_forget()
        lbly.grid(row=0,column=0,pady=5)
        i = False
    else:
        lbly.grid_forget()
        lblx.grid(row=0,column=0,pady=5)
        i = True

btn = tkinter.Button(win, text="Change", command=foo)
btn.grid(row=1, column=0)

win.mainloop()

# #!/usr/bin/python3
# # write tkinter as Tkinter to be Python 2.x compatible
# from tkinter import *
# def hello(event):
#     print("Single Click, Button-l") 
# def quit(event):                           
#     print("Double Click, so let's stop") 
#     import sys; sys.exit() 

# widget = Button(None, text='Mouse Clicks')
# widget.pack()
# widget.bind('<Button-1>', hello)
# widget.bind('<Double-1>', quit) 
# widget.mainloop()



# class Person:
#   def __init__(mysillyobject, name, age):
#     mysillyobject.name = name
#     mysillyobject.age = age

#   def myfunc():
#     print("Hello my name is ")

# p1 = Person("John", 36)
# p1.myfunc()