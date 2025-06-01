import socket
import datetime
import sys
import threading

client_sockets = []
server_running = True

def log(msg):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f"{time}: {msg}"
    with open('server.log', 'a') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

def handle_client(client_socket, client_addr):
    global client_sockets, server_running
    log(f"Клиент подключился: {client_addr}")
    client_sockets.append(client_socket)

    try:
        while server_running:
            data = client_socket.recv(1024)
            if not data:
                break

            client_msg = data.decode('utf-8').strip()
            if client_msg.lower() == 'shutdown':
                log("Сервер выключен командой клиента.")
                server_running = False
                break

            log(f"Получено от {client_addr}: {client_msg}")
            client_socket.sendall(data)
    except Exception as e:
        log(f"Ошибка с клиентом {client_addr}: {e}")
    finally:
        client_sockets.remove(client_socket)
        client_socket.close()
        log(f"Клиент {client_addr} отключился")

def start_server():
    global server_running

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 9090))
        server_socket.listen()
        log("Сервер запущен и ожидает подключений...")

        try:
            while server_running:
                try:
                    server_socket.settimeout(1)
                    client_socket, client_addr = server_socket.accept()
                    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            log("Сервер был выключен вручную.")
        finally:
            for client in client_sockets:
                client.close()
            log("Сервер завершил работу.")
            sys.exit(0)

if __name__ == '__main__':
    start_server()
