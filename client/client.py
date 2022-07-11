import json
import socket

class Client:

    is_login = None

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 8080)
        self.socket.connect(server_address)
        self.socket.setblocking(1)

        self.is_login = False
        self.register()



    def register(self):
        while not self.is_login:
            redistred = input("Register or login r/l: ")
            if redistred == "r":
                name = input("Print ur name: ")

                while True:
                    password = input("Print password")
                    password2 = input("repit password")
                    if password == password2:
                        break
                    print("encorrect password")

                request_json = json.dumps({
                    "user_name": name,
                    "type": "REGISTER",
                    "password": password
                })
                self.socket.send(request_json.encode('UTF-8'))
                ans = self.socket.recv(1024).decode('UTF-8')
                if ans == "REGISTERED":
                    print("u are registred in system")
                    self.is_login = True
            elif redistred == "l":
                name = input("Print ur name: ")
                password = input("Print password")

                request_json = json.dumps({
                    "user_name": name,
                    "type": "LOGIN",
                    "password": password
                })

                self.socket.send(request_json.encode('UTF-8'))

                ans = self.socket.recv(1024).decode("UTF-8")
                if ans == "LOGIN_ERROR":
                    print("Encorrect password")
                elif ans == "LOGIN":
                    print("U are loging in")
                    self.is_login = True

    def message(self):
        pass