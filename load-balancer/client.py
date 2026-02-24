import socket
import sys

sock = socket.socket()

try:
	sock.connect(('127.0.0.1', 8080))
	while True:
		message = input()
		sock.send(message.encode())
finally:
	sock.close()
