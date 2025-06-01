import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 9090)

    try:
        while True:
            message = input("Введите сообщение (или 'exit' для выхода): ")
            client_socket.sendto(message.encode(), server_address)

            if message.strip().lower() == 'exit':
                print("Клиент завершает работу.")
                break

            response, _ = client_socket.recvfrom(1024)
            print(f"Ответ от сервера: {response.decode()}")
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    finally:
        client_socket.close()

if __name__ == '__main__':
    udp_client()
