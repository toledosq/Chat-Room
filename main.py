#!/usr/bin/end python3

import tkinter as tk
import subprocess as sp


def create_server():
	top.withdraw()
	sp.call('python server_script.py')
	top.deiconify()


def join_server():
	top.withdraw()
	sp.call('python client_script.py')
	top.deiconify()


top = tk.Tk()
top.geometry("250x250")
top.resizable(0, 0)
top.title("What do")

select_frame = tk.Frame(top)

header = tk.Label(select_frame, text="What would you like to do?", justify=tk.CENTER)
create_server_btn = tk.Button(select_frame, text="Create Chat Room", width=25, height=2, command=create_server)
join_server_btn = tk.Button(select_frame, text="Join a Chat Room", width=25, height=2, command=join_server)

header.pack()
create_server_btn.pack()
join_server_btn.pack()

select_frame.pack_propagate(0)
select_frame.pack(fill=tk.BOTH, expand=1)

tk.mainloop()
