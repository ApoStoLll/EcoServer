import server as sv
host = '192.168.0.135'
port = 8080
name = 'kek'
serv = sv.LolHTTPServer(host, port, name)
try:
    serv.serve_forever()
except KeyboardInterrupt:
    print("CHO")
#https://github.com/ApoStoLll/EcoServer.git