from socket import *

## Arbitrary port number choice
serverPort = 8898

## Create socket to send/recieve information (under personal IP address, and specified port)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(("localhost",serverPort))

## Get user input
sentence = raw_input('\nCONNECTED!\nInput lowercase sentence: ')

## Send information to server
clientSocket.send(sentence.encode())

## Print message response from server
modifiedSentence = clientSocket.recv(1024)
print "\nFrom Server: %s" % modifiedSentence.decode()

## (Gracefully), close connection socket
clientSocket.close()