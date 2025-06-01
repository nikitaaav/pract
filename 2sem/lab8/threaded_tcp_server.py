import socket
import threading

def handle_client(conn, addr):
    print(f"[Threaded Server] Клиент подключён: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[Threaded Server] Получено от {addr}: {data.decode()}")
            conn.sendall(data)

def run_threaded_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9091))
    server.listen()
    print("[Threaded Server] Ожидание подключений...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
