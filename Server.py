import socket
from _thread import *

host = ''
port = 80
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
        data = conn.recv(2048)
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
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client, (conn,))