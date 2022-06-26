import socket
import json
import threading

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8080)
socket.connect(server_address)
socket.setblocking(1)

is_login = False

while not is_login:
    redistred = input("Register or login r/l: ")
    if redistred=="r":
        name = input("Print ur name: ")

        while True:
            password = input("Print password")
            password2 = input("repit password")
            if password==password2:
                break
            print("encorrect password")

        request_json = json.dumps({
            "user_name":name,
            "type":"REGISTER",
            "password":password
        })
        socket.send(request_json.encode('UTF-8'))
        ans = socket.recv(1024).decode('UTF-8')
        if ans=="REGISTERED":
            print("u are registred in system")
            is_login = True
    elif redistred=="l":
        name = input("Print ur name: ")
        password = input("Print password")

        request_json = json.dumps({
            "user_name": name,
            "type": "LOGIN",
            "password": password
        })

        socket.send(request_json.encode('UTF-8'))

        ans = socket.recv(1024).decode("UTF-8")
        if ans == "LOGIN_ERROR":
            print("Encorrect password")
        elif ans == "LOGIN":
            print("U are loging in")
            is_login = True

def get_meaages():
    while True:
        message = socket.recv(1024).decode("UTF-8")
        print(message)


tr = threading.Thread(target=get_meaages)
tr.start()

while True:
    a = input()
    request_json = json.dumps({
        "user_name": name,
        "type": "MESSAGE",
        "message": a
    })
    socket.send(request_json.encode("UTF-8"))
