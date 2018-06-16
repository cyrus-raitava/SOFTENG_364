import socket
# Create simple TCP socket
# NOTE: AF_INET refers to IPV4 address, and SOCK_STREAM refers to TCP (SOCK_DGRAM would be UDP)
## SURROUND socket statement with try/catch clause

try:

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, e:
	print("Socket creation failed with error: %s" %e)
	sys.exit(1)

# Since we are connecting over the internet (http), we will use port 80 (port 25 for sneding an email?)
port = 80

# Get the IP address of the desired URL (essentially DNS?)
## SURROUND statement resolving host name with try/catch clause

try:

	ip = socket.gethostbyname('www.google.com')
	print (ip)

except socket.gaierror, e:
	print("There was an error resolving the host: %s" %e)
	sys.exit(1)
except socket.error, e:
	print("Socket connection failed with error: %s" %e)
	sys.exit(1)

# Connect the socket to the local port, and the foreign server (ip)
s.connect((ip, port))
print ("The socket has successfully connected to Google on IP Address == %s" %(ip))

# Create a variable (message), which is to be sent via the created socket
message = "GET / HTTP/1.1\r\n\r\n"

# Send data to the google server using the sendall function
s.sendall (message)
print ("Message send successfully")

# Recieve the message from the google server, specifying the message buffer to be of size 4096 bytes (default is 1024)
reply = s.recv(16384)
print reply

# (Gracefully) close the socket created
s.close()
