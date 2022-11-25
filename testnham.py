# import tkinter
# import threading


# class meme:
#     x = 0

#     def __init__(self) -> None:
#         self.win = tkinter.Tk()

#         self.frm = tkinter.Frame(self.win)
#         self.frm.pack()

#         for i in range(10):
#             self.lbl = tkinter.Label(self.frm, text=f"{i}")
#             self.lbl.pack()

#         self.lbl = tkinter.Button(self.win, text="Hi am jack", command=self.foo)
#         self.lbl.pack()

#     # def foo(self):
#     #     if self.lbl['state'] == 'normal':
#     #         self.lbl["state"] = "disabled"
#     #         self.lbl.configure(disabledforeground='black')
#     #     ano = tkinter.Toplevel()
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

l = {
    "hiih" : "233",
    "kd" : "đ"
}
print(type(list(l)))

# class Person:
#   def __init__(mysillyobject, name, age):
#     mysillyobject.name = name
#     mysillyobject.age = age

#   def myfunc():
#     print("Hello my name is ")

# p1 = Person("John", 36)
# p1.myfunc()