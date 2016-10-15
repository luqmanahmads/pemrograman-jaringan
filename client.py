import socket
import sys

#inisialisasi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#koneksi
server_address = ('localhost', 11000)
print >>sys.stderr, 'connecting  to %s port %s'% server_address
client_socket.connect(server_address)

try:
	#send 
	message = "ini adalah message yang akan diterima client"
	print >>sys.stderr, 'sending "%s"'% message
	client_socket.sendall(message)
	
	#mencari respon
	amount_received = 0
	amount_expected = len(message)
	while amount_received < amount_expected:
		data = client_socket.recv(16)
		amount_received += len(data)
		print >>sys.stderr, 'received "%s"'% data
finally:
	print >>sys.stderr, 'closing socket'
	client_socket.close()
