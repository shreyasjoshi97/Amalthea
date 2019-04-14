import socket
import os
import threading
import StaticAnalysis
import DeltaCalculator
import AverageCalculator
import BehaviourChange
from _thread import *
#374
host = ''
port = os.environ.get("PORT", 50000)
port = int(port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

permissions_file = 'permissions.txt'
delta_file = 'delta.csv'
behaviour_file = 'behaviour.csv'
averages_file = 'averages.csv'


def delete_files():
    if os.path.exists(permissions_file):
        os.remove(permissions_file)
    if os.path.exists(averages_file):
        os.remove(averages_file)
    if os.path.exists(behaviour_file):
        os.remove(behaviour_file)


def init_file(message):
    delete_files()

    if "|" in message:
        print("Permissions process")
        file = open(permissions_file, "a")
        return file
    elif "+" in message:
        print("Average process")
        file = open(averages_file, "a")
        file.write("\"Name\",\"CPU\",\"VSS\",\"RSS\",\"PCY\",\"Time\"\n")
        return file
    # elif "+" in message:
    #     print("Average process")
    #     file = open(averages_file, "a")
    #     file.write("\"Name\",\"active_cpu_q1\",\"active_cpu_q2\",\"active_cpu_q3\","
    #                "\"idle_cpu_q1\",\"idle_cpu_q2\",\"idle_cpu_q3\","
    #                "\"active_mem_q1\",\"active_mem_q2\",\"active_mem_q3\","
    #                "\"idle_mem_q1\",\"idle_mem_q2\",\"idle_mem_q3\"\n")
        return file
    elif "~" in message:
        print("Behaviour process")
        file = open(behaviour_file, "a")
        file.write("\"Name\",\"active_cpu_q1\",\"active_cpu_q2\",\"active_cpu_q3\","
                   "\"idle_cpu_q1\",\"idle_cpu_q2\",\"idle_cpu_q3\","
                   "\"active_mem_q1\",\"active_mem_q2\",\"active_mem_q3\","
                   "\"idle_mem_q1\",\"idle_mem_q2\",\"idle_mem_q3\"\n")
        return file


def parse_data(message):
    f = init_file(message)
    start_reading = False
    for x in message:
        if start_reading:
            if x == "$":
                f.write("\n")
            else:
                f.write(x)
        if x == "|" or x == "^" or x == "+" or x == "~":
            start_reading = True
    try:
        f.close()
        result = setup_analysis()
    except AttributeError as ex:
        print("Attribute Error: ", ex)
        return "{}"
    return result


def setup_analysis():
    results = ''
    if os.path.exists(permissions_file):
        print("HERE")
        static = StaticAnalysis.StaticAnalysis()
        results = static.initialise_results()
    # if os.path.exists(delta_file):
    #     delta = DeltaCalculator.DeltaCalculator()
    #     results = delta.begin_analysis()
    if os.path.exists(averages_file):
        average = AverageCalculator.AverageCalculator()
        results = average.begin_analysis()
    if os.path.exists(behaviour_file):
        behaviour = BehaviourChange.BehaviourChange()
        results = behaviour.begin_analysis()
    delete_files()
    return str(results)


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
            data = conn.recv(2048)
            data_holder = data_holder + data.decode('utf-8')
            for string in data_holder:
                if string == '\n':
                    # ret1 = "Result Start " + parse_data(data_holder) + " Result End"
                    # print(ret1)
                    # ret = data_holder + "\n" + ret1
                    # reply = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + parse_data(data_holder) + "\n\n"
                    reply = parse_data(data_holder) + "\n"
                    open = conn.fileno()

                    if open != -1:
                        conn.sendall(str.encode(reply))

                    #print(ret)
                    if not data:
                        print("No data received")
                        break
                    data_holder = ''
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
