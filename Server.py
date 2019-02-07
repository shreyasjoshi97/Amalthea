import socket
import os
import pandas as pd
from _thread import *
import BehaviourInit
import StaticInit


def init_file(name):
    if os.path.exists(name):
        os.remove(name)
    file = open(name, "a")
    return file


def setup_analysis():
    if os.path.exists(permissions_file):
        static = StaticInit.StaticInit()
        results = static.initialise_results()
    if os.path.exists(behaviour_file):
        behaviour = BehaviourInit.BehaviourInit()
    return results


host = '0.0.0.0'
permissions_file = 'permissions.txt'
behaviour_file = 'behaviour.csv'
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
            reading = False
            data = conn.recv(1024)
            data_holder = data_holder + data.decode('utf-8')
            for string in data_holder:
                if string == '~':
                    results = setup_analysis()
                    reply = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + str(results) + "\n"
                    conn.sendall(str.encode(reply))
                    # print(data_holder)
                    if not data:
                        print("No data received")
                        break
                    reading = False
                    sending = False
                    break
                elif string == '|':
                    reading = True
                    f = init_file(permissions_file)
                elif string == '^':
                    f = init_file(behaviour_file)
                    f.write("\"PID\",\"USER\",\"PR\",\"NI\",\"CPU\",\"S\",\"#THR\",\"VSS\",\"RSS\",\"PCY\",\"Name\",\"Time\"\n")

                if reading:
                    print(string)
                    f.write(string)

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