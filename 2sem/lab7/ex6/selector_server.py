import selectors
import socket

selector = selectors.DefaultSelector()
server_running = True  # Глобальный флаг завершения сервера

def accept_connection(server_socket):
    try:
        client_socket, client_address = server_socket.accept()
        print(f"[+] Подключение от {client_address}")
        client_socket.setblocking(False)
        selector.register(client_socket, selectors.EVENT_READ, send_echo)
    except Exception as e:
        print(f"[!] Ошибка при accept: {e}")

def send_echo(client_socket):
    global server_running
    try:
        data = client_socket.recv(1024)
        if data:
            message = data.decode().strip()
            print(f"[=] Получено: {message}")

            # Обработка команды shutdown
            if message.lower() == 'shutdown':
                print("[!] Получена команда shutdown. Завершение работы сервера.")
                server_running = False
                return

            client_socket.sendall(data)  # Эхо
        else:
            print("[~] Клиент отключился")
            selector.unregister(client_socket)
            client_socket.close()
    except ConnectionResetError:
        print("[!] Клиент закрыл соединение принудительно")
        selector.unregister(client_socket)
        client_socket.close()
    except Exception as e:
        print(f"[!] Ошибка обработки клиента: {e}")
        selector.unregister(client_socket)
        client_socket.close()

def start_server():
    global server_running

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    server_socket.setblocking(False)

    selector.register(server_socket, selectors.EVENT_READ, accept_connection)
    print("[*] Сервер запущен на порту 9090. Ожидание подключений...")

    try:
        while server_running:
            events = selector.select(timeout=1)
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        print("\n[!] Остановка по Ctrl+C")
    finally:
        print("[*] Завершение работы сервера...")
        # Закрытие всех клиентов
        for key in selector.get_map().values():
            sock = key.fileobj
            try:
                selector.unregister(sock)
                sock.close()
            except Exception:
                pass
        selector.close()
        print("[*] Сервер остановлен")

if __name__ == '__main__':
    start_server()
