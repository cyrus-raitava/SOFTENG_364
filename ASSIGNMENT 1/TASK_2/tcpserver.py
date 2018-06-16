from socket import *
import threading

## Create method to send capitalized, formatted message back to client on particular socket
def sentenceLower(connectionSocket, clientNumber) :

    ## Recieve data from client
    sentence = connectionSocket.recv(1024).decode()

    ## Change data to uppercase
    capitalizedSentence = sentence.upper()

    ## Note to server, what interaction has been
    print "Client %i: %s ----> %s" % (clientNumber, sentence, capitalizedSentence)

    ## Format and send the intended message to the same client
    message = "Hi Client %i!\nHere is your message, capitalized: %s\n" % (clientNumber, capitalizedSentence)
    connectionSocket.send(message.encode())
    connectionSocket.close()

    ## Increment the number of clients
    clientNumber = clientNumber + 1

## Create method to deal with thread handling of multiple clients
def threadGenerator() :

    clientNumber = 1

    ## Bloacking-code to increment number of threads,
    while(True) :
        connectionSocket, addr = serverSocket.accept()

        ## Create and begin new thread for every client connected
        thread = threading.Thread(target=sentenceLower, args=(connectionSocket, clientNumber))
        print "Client %i connected!" % clientNumber
        thread.start()

        ## Increment number of clients
        clientNumber = clientNumber + 1

## Begin server on arbitrary port number
serverPort = 8898

## Create socket object, and bind it to listen to the port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


## Print intro lines
print('==================================')
print('Server beginning on port 8898...')
print('The system is ready to begin! ')
print('==================================')

## Call threading method
threadGenerator()
