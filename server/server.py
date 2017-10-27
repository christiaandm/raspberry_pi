# server.py
import socket
import time
import threading
import datetime
import os

serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
# host = socket.gethostname()
host = "192.168.42.1"

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)
connected_clients = dict()
next_command = ""
received_status = ""

def background_check():
    """thread background_check function"""
    while True:
        for ip in dict(connected_clients):
            # als een connectie 5 seconden niet meer gezien is
            current_time_check = round(time.time())-5
            if (current_time_check > connected_clients[ip]["last_time"]):
                last_seen = datetime.datetime.fromtimestamp(
                    connected_clients[ip]["last_time"]
                ).strftime('%Y-%m-%d %H:%M:%S')
                print("Alarm: Verbinding verbroken: " + ip + " Laatst gezien: " + str(last_seen))
            time.sleep(1)
background_thread = threading.Thread(target=background_check)
background_thread.start()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def cli():
    while True:
        global next_command
        cls()
        print("1: alarm uit zetten")
        print("2: alarm af laten gaan")
        print("3: alarm status tonen")

        try:
            choice = int(input("Kies een optie:"))
        except:
            continue
        if choice == 1:
            next_command = "set_status:standby"
        elif choice == 2:
            next_command = "set_status:on"
        elif choice == 3:
            print("alarm status: " + received_status)
            input("Druk op enter om verder te gaan")


cli_thread = threading.Thread(target=cli)
cli_thread.start()

try:
    while True:
        # establish a connection
        clientsocket,addr = serversocket.accept()
        current_time = round(time.time())
        ip = addr[0]

        if ip not in connected_clients:
            connected_clients[ip] = dict()

        connected_clients[ip]['last_time'] = current_time
        # print("Got a connection from %s" % str(addr))
        received_status = clientsocket.recv(1024).decode('ascii')
        # print("recieved_message: {}".format(recieved_message))
        string = str(current_time) + ' \n'
        if next_command != "":
            string = next_command
            next_command = ""

        clientsocket.send(string.encode('ascii'))
        clientsocket.close()
except socket.error:
    #write error code to file
    pass
finally:
    serversocket.close()
serversocket.close()