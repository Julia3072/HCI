import serial
import socket

ser = serial.Serial("/dev/cu.usbmodem1421", 9600)  # Establish the connection on a specific port

HOST, PORT = '', 9600

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...')

while True:
    data = ser.readline()
    print("RECV {}".format(data))

    client_connection, client_address = listen_socket.accept()

    client_connection.send(data)

    request = client_connection.recv(1024)

    try:
        data = str(int(str(request).replace("\\n", "").replace("b", "").replace("\'", "")))
        print(data.encode('ascii'))
        ser.write(data.encode('ascii'))
    except ValueError:
        client_connection.close()

    client_connection.close()