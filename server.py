import socket
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_socket.bind(('127.0.0.1', 53210))
serv_socket.listen()