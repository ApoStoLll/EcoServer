import socket
import threading

def run_server(port=8080):
    server_socket = create_server_socket(port)
    client_id = 0
    while True:
        client_socket = accept_client_connection(server_socket, client_id)
        t = threading.Thread(target=serve_client, args=(client_socket, client_id))
        t.start()
        client_id += 1
        #serve_client(client_socket, client_id)

def serve_client(client_socket, client_id):
    request = read_request(client_socket)
    if request is None:
        print(f'Client #{client_id} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(client_socket, response, client_id)

def read_request(client_socket):
    request = bytearray()
    try:
        while True:
            chunk = client_socket.recv(4)
            if not chunk: 
                return None #Client unexpectedly disconnected
            request += chunk
            return request
    except ConnectionResetError:
        return None #Pizda
    except:
        raise #генерирует исключение

def handle_request(request):
    print(request)
    return request
    #obrabotka

def write_response(client_socket, response, client_id):
    client_socket.sendall(response)
    client_socket.close()
    print(f'Client #{client_id} has been served')

def create_server_socket(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    server_socket.bind(('192.168.0.135', server_port))
    server_socket.listen()
    return server_socket

def accept_client_connection(serv_socket, client_id):
    client_socket, client_address = serv_socket.accept()
    print(f'Client #{client_id} connected')
    return client_socket

run_server()
#serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
#serv_socket.bind(('192.168.0.135', 8080))
#serv_socket.listen(10)
#while True:
#    client_sock, client_address = serv_socket.accept()
#    print("Connected by", client_address)
#    while True:
#        data = client_sock.recv(1024)
#        print("POLUCHENO", data)
#        if not data:
#            break
#        client_sock.sendall(b"KEK")
#    client_sock.close()