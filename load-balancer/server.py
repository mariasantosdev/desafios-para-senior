import socket

MAX_CONNECTIONS = 10
s = socket.socket()
s.bind(('127.0.0.1',8085))

s.listen(MAX_CONNECTIONS)

try:
	conn, address = s.accept()
	while True:
		data = conn.recv(200)
		print(data)
finally:
	conn.close()
	s.close()
