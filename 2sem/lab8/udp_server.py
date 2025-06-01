import socket

def run_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(('localhost', 9092))
        print("[UDP Server] Ожидание сообщений...")
        while True:
            data, addr = server.recvfrom(1024)
            print(f"[UDP Server] Получено от {addr}: {data.decode()}")
            server.sendto(data, addr)
