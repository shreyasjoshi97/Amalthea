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


def parse_data(message):
    start_reading = False
    data = ''
    for x in message:
        if start_reading:
            data += x
        if x == "|":
            start_reading = True
    return data


def threaded_client(conn):
    data_holder = ''
    sending = True
    while sending:
        try:
            data = conn.recv(1024)
            data_holder = data_holder + data.decode('utf-8')
            for string in data_holder:
                if string == '\n':
                    ret1 = parse_data(data_holder)
                    print(ret1)
                    ret = data_holder + "\n" + ret1
                    reply = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + ret + "\n"
                    # reply = data_holder
                    conn.sendall(str.encode(reply))
                    #print(ret)
                    if not data:
                        print("No data received")
                        break
                    sending = False
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
