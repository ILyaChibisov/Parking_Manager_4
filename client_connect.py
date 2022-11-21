from socket import socket, AF_INET, SOCK_STREAM
from Constant import IP_SERVER, LOCALHOST


def client_connect(message):

    CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCKET.connect((IP_SERVER, 5020))
    CLIENT_SOCKET.send(message.encode('utf-8'))
    answer = CLIENT_SOCKET.recv(8192)
    print(answer.decode('utf-8'))
    CLIENT_SOCKET.close()
    return answer.decode('utf-8')

