import socket
import datetime

def log(message):
    """Простая функция логирования с меткой времени."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def handle_client(client_socket, client_address):
    """Обрабатывает подключение от одного клиента (однопоточно)."""
    log(f"Подключён клиент: {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                log(f"Клиент {client_address} закрыл соединение")
                break
            log(f"Получено от {client_address}: {data.decode('utf-8', errors='replace')}")
            client_socket.sendall(data)
    except ConnectionResetError:
        log(f"Клиент {client_address} оборвал соединение")
    except Exception as e:
        log(f"Ошибка при работе с клиентом {client_address}: {e}")
    finally:
        client_socket.close()
        log(f"Соединение с {client_address} закрыто")

def start_server():
    """Запускает сервер в однопоточном режиме."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    log("Сервер запущен и ожидает подключения...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
    except KeyboardInterrupt:
        log("Сервер остановлен вручную")
    finally:
        server_socket.close()
        log("Сервер выключен")

if __name__ == '__main__':
    start_server()
