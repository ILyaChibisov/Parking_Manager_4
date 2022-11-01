from socket import socket, AF_INET, SOCK_STREAM


def client_connect(message):

    CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCKET.connect(('localhost', 5020))
    CLIENT_SOCKET.send(message.encode('utf-8'))
    answer = CLIENT_SOCKET.recv(4096)
    print(answer.decode('utf-8'))
    CLIENT_SOCKET.close()
    return answer.decode('utf-8')


# client_connect('Привет сервер')
