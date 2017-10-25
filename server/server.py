# server.py
import socket
import time
import threading

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9991

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)
connected_clients = dict()

def background_check():
    """thread background_check function"""
    while True:
        for ip in connected_clients:
            time2 = round(time.time())-5
            if (time2 > connected_clients[ip]["last_time"]):
                print("Connection lost: " + ip + str(connected_clients[ip]["last_time"]))
            time.sleep(1)
background_thread = threading.Thread(target=background_check)
background_thread.start()

def cli():
    status = input("voeer een status in:")

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
        print("Got a connection from %s" % str(addr))
        recieved_message = clientsocket.recv(1024).decode('ascii')
        print("recieved_message: {}".format(recieved_message))
        string = str(current_time) + ' \n'

        if recieved_message == "on":
            string = "set_status:standby"

        clientsocket.send(string.encode('ascii'))
        clientsocket.close()
except socket.error:
    #write error code to file
    pass
finally:
    serversocket.close()