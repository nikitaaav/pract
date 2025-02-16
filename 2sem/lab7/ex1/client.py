import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 9090))
        while True:
            data = input("Введите сообщение для отправки: ")
            if data == 'exit':
                break
            client_socket.sendall(data.encode('utf-8'))
            response = client_socket.recv(1024)
            print(f"Ответ от сервера: {response.decode('utf-8')}")
    except ConnectionRefusedError:
        print("Сервер не запущен или недоступен")
    except ConnectionResetError:
        print("Соединение разорвано!")
    except socket.timeout:
        print("Таймаут соединения!")
    finally:
        client_socket.close()

start_client()
