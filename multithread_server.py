import threading
import socket
import sys

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
server_address = ('localhost', 11001)
print >>sys.stderr, "starting up on %s port %s" % server_address
sock.bind(server_address)

#listening
sock.listen(1)

#fungsi untuk melayani client
def layani_client(koneksi_client,alamat_client):
	try: 
		print >>sys.stderr, "ada koneksi dari ", alamat_client
		while True:
			message = koneksi_client.recv(16)
			if message:
				print >>sys.stderr, "data diterima ", message
				koneksi_client.send(message)
			else:
				break
	finally:
		koneksi_client.close()


while True:
	#waiting for connection
	print >>sys.stderr, "waiting for connection"
	koneksi_client, alamat_client = sock.accept()
	
	s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	s.start()
