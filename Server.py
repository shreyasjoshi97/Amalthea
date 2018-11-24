import socket
import os
import re
from _thread import *

host = '0.0.0.0'
port = os.environ.get("PORT", 5000)
port = int(port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((host, port))
except socket.error as e:
    print("Binding failed" + e.strerror)

s.listen(1)
print('Server listening')


def threaded_client(conn):
    data_holder = ''
    sending = True
    while sending:
        try:
            data = conn.recv(1024)
            data_holder = data_holder + data.decode('utf-8')
            for string in data_holder:
                if string == '\n':
                    data_holder = data_holder + conn.recv(1024).decode('utf-8')
                    print("Newline found" + data_holder)
                    reply = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + data_holder
                    # reply = data_holder
                    conn.send(str.encode(reply))
                    print(data_holder)
                    if not data:
                        print("No data received")
                        break
                    sending = False
                    conn.close()
        except BrokenPipeError as e:
            print("Socket error: ", e)
            break
        except ConnectionResetError as e:
            print("Connection reset error")
            break
    conn.close()


while True:
    conn, addr = s.accept()
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client, (conn,))
