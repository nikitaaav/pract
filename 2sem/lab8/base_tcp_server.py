import socket

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', 9090))
        server.listen()
        print("[TCP Server] Ожидание подключения клиента...")
        conn, addr = server.accept()
        with conn:
            print(f"[TCP Server] Клиент подключён: {addr}")
            data = conn.recv(1024)
            print("[TCP Server] Получено:", data.decode())
            conn.sendall(data)
