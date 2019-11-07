import socket
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_socket.bind(('127.0.0.1', 53210))
serv_socket.listen(10)
while True:
    client_sock, client_address = serv_socket.accept()
    print("Connected by", client_address)
    while True:
        data = client_sock.recv(1024)
        print("POLUCHENO", data)
        if not data:
            break
        client_sock.sendall(b"KEK")
    client_sock.close()