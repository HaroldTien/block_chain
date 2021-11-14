import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    clientsocket,adderss=s.accept()
    print('connection from',adderss,'has been established!')
    clientsocket.send(bytes('welcome to the server!','utf-8'))