import socket

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('localhost', 9090))
        msg = input("Введите сообщение: ").encode()
        client.sendall(msg)
        data = client.recv(1024)
        print("[TCP Client] Ответ от сервера:", data.decode())
