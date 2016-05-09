import serial
import socket

ser = serial.Serial("/dev/cu.usbmodem1421", 9600)

HOST, PORT = '', 3001

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    try:
        data = str(str(request).replace("\\n", "").replace("b", "").replace("\'", ""))
        print(data.encode('ascii'))
        ser.write(data.encode('ascii'))

    except ValueError:
        print()

    client_connection.close()
