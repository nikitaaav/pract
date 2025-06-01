import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 9090))
        while True:
            data = input("Введите сообщение для отправки: ")
            if data.lower() == 'exit':
                break
            client_socket.sendall(data.encode('utf-8'))
            response = client_socket.recv(1024)
            if response == b'':
                print("Соединение закрыто сервером.")
                break
            print(f"Ответ от сервера: {response.decode('utf-8')}")
    except KeyboardInterrupt:
        print("\nРабота клиента была прервана пользователем.")
    except ConnectionRefusedError:
        print("Сервер не запущен или недоступен.")
    except ConnectionResetError:
        print("Соединение разорвано сервером!")
    except socket.timeout:
        print("Таймаут соединения!")
    finally:
        client_socket.close()
        print("Клиент завершил работу.")

if __name__ == '__main__':
    start_client()
