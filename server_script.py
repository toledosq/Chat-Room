#!/usr/bin/end python3

"""
Name: server_script.py
Author: Christopher Smith
Description: This script initiates the chat server using TCP sockets
"""

# IMPORTS ------------------------------------------------------------#
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import xml.etree.ElementTree as ET
import time
import sys
import itertools as IT


# CONSTANTS ----------------------------------------------------------#
HOST = ''
PORT = 55555
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
BUFSIZE = 1024
START_MSG = "Welcome to the chat! Please enter name to continue: "
DONE=False


# CONNECTIONS RECORD -------------------------------------------------#
clients = {}
addresses = {}


# HELPER FUNCTIONS ---------------------------------------------------#
def incoming_client():
    """ Accept client and get username. Start client thread. """
    global DONE
    while True:
        client, client_address = SERVER.accept() 
        DONE=True
        time.sleep(0.2)
        print("%s:%s has connected." % client_address)
        client.send(bytes(create_msg(START_MSG)))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """ Listen for client communication and broadcast to others """
    # Receive client's name and add to record
    name = client.recv(BUFSIZE).decode("utf8")
    if name == "\q":
    	client.close()
    	print("%s:%s has disconnected." % addresses[client])
    	return
    	
    clients[client] = name

    # Welcome client to chat
    welcome_msg = "Welcome %s!" % name
    client.send(bytes(create_msg(welcome_msg)))

    # Broadcast client name to room
    msg = "%s has joined the chat" % name
    broadcast(bytes(create_msg(msg)))

    # Update client list
    broadcast_clients()

    # Wait for client communication
    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes("\q", "utf8"):
            broadcast(bytes(create_msg(name + ": " + msg.decode("utf-8"))))
        else:
            client.close()
            print("%s:%s has disconnected." % addresses[client])
            del clients[client]
            broadcast(bytes(create_msg("%s has left the chat." % name)))
            broadcast_clients()
            break


def broadcast(msg):
    for sock in clients:
        sock.send(bytes(msg))


def broadcast_clients():
    """ Send XML object containing all active usernames to each client """
    root = ET.Element("data")
    client_tag = ET.SubElement(root, "client")

    for idx in clients:
        ET.SubElement(client_tag, "name").text = clients[idx]

    broadcast(bytes(ET.tostring(root)))


def create_msg(body=None, name=None):
    """ Create an XML object to send to clients """
    root = ET.Element("data")
    msg_tag = ET.SubElement(root, "msg")
    ET.SubElement(msg_tag, "body").text = body
    return ET.tostring(root)


def animate():
    for i in IT.cycle(['|', '/', '-', '\\']):
        global DONE
        if DONE:
            break
        sys.stdout.write('\rWaiting for a client... ' + i)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rWaiting for a client... Done\n')


# START SERVER AND LISTEN FOR CONNECTIONS ----------------------------#
if __name__ == "__main__":
    SERVER.listen(10)
    t = Thread(target=animate)
    t.start()
    ACCEPT_THREAD = Thread(target=incoming_client)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
