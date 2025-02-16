import socket
from socket import SocketIO


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    print("Сервер запущен и ожидает подключений...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Клиент подключился: {client_address}")

            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
                break
            finally:
                client_socket.close()
                print(f"Клиент {client_address} отключился")
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()
        print("Сервер отключен")

start_server()
