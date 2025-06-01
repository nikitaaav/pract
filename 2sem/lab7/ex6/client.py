import socket

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 9090))
        while True:
            msg = input("Введите сообщение (или 'shutdown'): ")
            sock.sendall(msg.encode())
            if msg.strip().lower() == 'shutdown':
                print("[!] Команда shutdown отправлена. Клиент завершает работу.")
                break
            response = sock.recv(1024)
            print("Ответ сервера:", response.decode())

if __name__ == '__main__':
    client()
