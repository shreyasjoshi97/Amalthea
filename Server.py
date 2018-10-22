import socket
import errno
import os
from _thread import *

host = '0.0.0.0'
port = os.environ.get("PORT", 5000)
port = int(port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print('Waiting for connection')

def threaded_client(conn):
    conn.send(str.encode('Welcome, type your info\n'))
    dataHolder = ''
    while True:
        try:
            data = conn.recv(1024)
            dataHolder = dataHolder + data.decode('utf-8')
            for string in dataHolder:
                if string == '\n':
                    reply = 'Server output: ' + dataHolder + '\n'
                    conn.sendall(str.encode(reply))
                    serverOutput = addr[0] + ': ' + dataHolder
                    dataHolder = ''
                    print(serverOutput)
                    if not data:
                        break
        except BrokenPipeError as e:
            print("Socket error: ", e)
        except ConnectionResetError as e:
            print("Connection reset error")
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client, (conn,))