import socket

def run_udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        server_address = ('localhost', 9092)
        msg = input("Введите сообщение: ").encode()
        client.sendto(msg, server_address)
        data, _ = client.recvfrom(1024)
        print("[UDP Client] Ответ от сервера:", data.decode())
