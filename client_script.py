#!/usr/bin/end python3

"""
Name: client_script.py
Author: Christopher Smith
Description: This script handles client-side of chat room
"""

# IMPORTS ------------------------------------------------------------#
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import xml.etree.ElementTree as ET


# CONSTANTS ----------------------------------------------------------#
HOST = input('Enter host: ')
PORT = 55555
COLOR = "#ddeaff"
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)


# HELPER METHODS -----------------------------------------------------#
def receive():
    """ Parse an XML msg from server and send to appropriate widget """
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            formatted_msg = "<root>" + msg + "</root>"
            
            tree = ET.fromstring(formatted_msg)

            for data in tree.iter('data'):
                for child in data:
                    if child.tag == "client":
                        client_list.delete(0, tkinter.END)
                        for name in child.iter(tag="name"):
                            client_list.insert(tkinter.END, u"\u25C9 " + name.text)
                    elif child.tag == "msg":
                        for body in child.iter(tag="body"):
                            msg_list.insert(tkinter.END, body.text)

        except OSError:
            break


def send(msg="", event=None):
    """ Send msg to server. If msg is {q} then close socket and GUI """
    connected = True
    attempt = 0

    while connected:
        try:
            client_socket.send(bytes(msg, "utf-8"))
            break
        except ConnectionResetError:
            # If client can't contact server 3 times, send failed
            attempt += 1
            if attempt == 3:
                connected = False
                msg_list.insert(tkinter.END, "No connection to server could be established. Please try again later.")

    if msg == "\q":
        client_socket.close()
        top.quit()


def on_close(event=None):
    """ If user exits client, send {q} to close connection """
    my_msg.set("\q")
    get_text()


def get_text(event=None):
	msg = my_msg.get()
	if len(msg) >= 200:
		#TODO: AlertDialog
		pass
	else:
		my_msg.set("")
		curr_chars.set("0")
		send(msg, event)


# CLIENT GUI ---------------------------------------------------------#
def update(event=None):
    curr_chars.set(str(len(my_msg.get())))

top = tkinter.Tk()
top.title("Chat room")
top.configure(background=COLOR)

message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")

scrollbar = tkinter.Scrollbar(message_frame)
msg_list = tkinter.Listbox(message_frame)
msg_list.configure(activestyle="none", selectbackground="white", selectforeground="black", height=16, width=128, yscrollcommand=scrollbar.set)
client_list = tkinter.Listbox(message_frame)
client_list.configure(activestyle="none", selectbackground="white", selectforeground="black", height=16, width=32, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
client_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
message_frame.pack()

curr_chars = tkinter.StringVar()
curr_chars.set("0")

text_frame = tkinter.Frame(top)
entry_field = tkinter.Entry(text_frame, width=96, textvariable=my_msg)
send_button = tkinter.Button(text_frame, width=16, text="Send", command=send)
char_count = tkinter.Label(text_frame, background=COLOR, textvariable=curr_chars)
char_total = tkinter.Label(text_frame, background=COLOR, text="/200")

entry_field.bind("<Return>", get_text)
entry_field.bind("<KeyPress>", update)

entry_field.pack(side=tkinter.LEFT, fill=tkinter.X)
send_button.pack(side=tkinter.LEFT)
char_count.pack(side=tkinter.LEFT)
char_total.pack(side=tkinter.LEFT)
text_frame.pack()

top.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()

    tkinter.mainloop()
