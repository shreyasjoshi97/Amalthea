import socket
import os
import re
import StaticInit
from _thread import *

host = '0.0.0.0'
port = os.environ.get("PORT", 5000)
port = int(port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
permissions_file = 'permissions.txt'
behaviour_file = 'behaviour.csv'


def init_file(name):
    file = open(name, "a")
    return file


def parse_data(message):
    f = ''
    start_reading = False
    data = ''
    for x in message:
        if start_reading:
            data += x
        if x == "|":
            start_reading = True
            f = init_file(permissions_file)
    f.write(data)
    result = setup_analysis()
    return result


def setup_analysis():
    results = ''
    if os.path.exists(permissions_file):
        static = StaticInit.StaticInit()
        results = static.initialise_results()
    # if os.path.exists(behaviour_file):
        # behaviour = BehaviourInit.BehaviourInit()
    return results


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
                    ret1 = "Result Start " + parse_data(data_holder) + " Result End"
                    print(ret1)
                    ret = data_holder + "\n" + ret1
                    reply = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + ret + "\n\n"
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
