# client.py
import socket


def send_ping(status):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    # host = socket.gethostname()

    host = "192.168.42.1"
    port = 9999
    s.settimeout(2)
    # connection to hostname on the port.
    s.connect((host, port))

    s.send(status.encode(encoding='UTF-8'))
    # Receive no more than 1024 bytes
    tm = s.recv(1024)

    s.close()
    return tm.decode('ascii')