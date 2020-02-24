import socket
import sys
import threading
import dbManager
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

MAX_LINE = 64*1024
MAX_HEADERS = 100

class LolHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            client_id = 0
            while True:
                conn, _ = server_socket.accept()
                try:
                    print("kk")
                    #self.serve_client(conn)
                    t = threading.Thread(target=self.serve_client, args=(conn, client_id))
                    t.start()
                    client_id += 1
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            server_socket.close()
    
    def serve_client(self, conn, client_id):
        try:
            req = self.parse_request(conn)
            #print("REQUEST FROM", client_id," ", req)
            resp = self.handle_request(req)
            #print("RESPONSE")
            print("RESPONSE ", resp)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
        if conn:
            conn.close()

    def parse_request(self, conn):
        print("parsing")
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile) 
        print("HEADERS: ", headers)
        host = headers.get('Host')
        print("HOST ", host)
        #if not host:
        #    raise Exception("Bad request")
        #if host not in (self._server_name, f'{self._server_name}:{self._port}'):
        #    raise Exception('Not found')
        print("REQUEST : ")
        req = Request(method, target, ver, headers, rfile)
        print(req.path)
        print(req.query)
        return req

    def parse_request_line(self, rfile):
        print("Parsing 2")
        raw = rfile.readline(MAX_LINE + 1)
        print("Raw: ", raw)
        if len(raw) > MAX_LINE:
            print("HUINA")
            raise Exception('Request line is too long')
        #print("skip if")
        request_line = str(raw, 'iso-8859-1')
        print(request_line)
        request_line = request_line.rstrip('\r\n')
        words = request_line.split()
        print("WORDS ", words)
        #if len(words) != 3:
        #    raise Exception('Malformed request line')
        #method, target, ver = words
        #if words[2] != 'HTTP/1.1':
         #   raise Exception('Unexpected HTTP version')
        return words

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline()
            if not line:
                break
            if len(line) > MAX_LINE:
                raise Exception('Header line is too long')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')
        if headers:
            sheaders = b''.join(headers).decode('iso-8859-1')
        # print("SHADERS ", sheaders)
            kek = Parser().parsestr(sheaders)
            print("PARS: ", kek)
            return kek
        else:
            return {'headed': 'no head'}

    def handle_request(self, req):
        db = dbManager.dbManager()
        if req.path == '/users': #and req.method == 'POST':
            return self.create_user(req, db)
        if req.path == '/user':
            return self.checkUser(req, db)
        #return Response(200, 'OK')
        raise Exception('Not found')
    
    def checkUser(self, req, db):
        user = db.getUser(req.query['username'][0], req.query['password'][0])
        if user is None:
            return Response(404, "User not found")
        else:
            return Response(200, 'OK')

    def create_user(self, req, db):
        print("CREATING USER")
        db.addUser(req.query['username'][0], req.query['name'][0], req.query['password'][0], req.query['email'][0])
        return Response(204, 'Created')

    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))
        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
        wfile.write(b'\r\n')
        print("RESPONSE ", resp)
        if resp.body:
            wfile.write(resp.body)
        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        return 0 #do smth

class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

class Response:
  def __init__(self, status, reason, headers=None, body=None):
    self.status = status
    self.reason = reason
    self.headers = headers
    self.body = body