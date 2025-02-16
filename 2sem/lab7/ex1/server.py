import socket
import threading
import datetime

stop_event = threading.Event()

def log(msg):
    time = datetime.datetime.now()
    msg = time.strftime("%Y-%m-%d %H:%M:%S") + ": " + msg
    with open('server.log', 'a') as f:
        f.write(msg + '\n')
        f.flush()
    print(msg)

def handle_client(client_socket, client_addr):
    """
    Функция для обработки каждого клиента
    :param client_socket: сокет соединения с клиентом
    :param client_addr: адрес клиента
    """

    try:
        while not stop_event.is_set():
            client_socket.settimeout(1)
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                msg = f"{data.decode('utf-8')} was sent by {client_addr[0]}:{client_addr[1]}"
                log(msg)
                client_socket.sendall(data)
            except Exception as e:
                continue
    except Exception as e:
        log(e.__str__())
    finally:
        client_socket.close()
        print(f"Клиент {client_addr} отключился")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    log("сервер запущен и ожидает подключений...")

    client_threads = []

    try:
        while not stop_event.is_set():
            try:
                server_socket.settimeout(1)
                client_socket, client_addr = server_socket.accept()
            except socket.timeout:
                continue

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            client_thread.start()
            client_threads.append(client_thread)
            log(f"клиент подключился: {client_addr}")
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        for t in client_threads:
            t.join()
        server_socket.close()
        log("сервер отключен")

start_server()
