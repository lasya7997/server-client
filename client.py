"""client.py file"""
import socket
import sys

print("Welcome to file management client. ")


try:
    SOC = socket.socket()
    HOST = '127.0.0.1'
    PORT = 8080

    SOC.connect((HOST, PORT))
except:
    print("Error connecting to server")
    sys.exit()

print("Press commands to know all the commands or press quit to quit.")
commands = []
while True:
    INP = input("-> ")
    if INP == "":
        print("Invalid command")
        continue
    if INP == "issued":
        print('\n'.join(commands))
    elif INP == "clear":
        commands = []
    elif INP != "quit":
        commands.append(INP)
        SOC.send(str.encode(INP))
        RESP = SOC.recv(4096)
        print("Server -> " + str(RESP, "utf-8"))
    else:
        SOC.send(str.encode(INP))
        RESP = SOC.recv(4096)
        print("Server -> " + str(RESP, "utf-8"))
        sys.exit()
