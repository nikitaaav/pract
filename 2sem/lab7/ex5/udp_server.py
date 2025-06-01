import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 9090))

    print("UDP сервер запущен и ожидает сообщений...")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        decoded_message = message.decode()

        print(f"Получено от {client_address}: {decoded_message}")

        if decoded_message.strip().lower() == 'exit':
            print("Получена команда на завершение. Сервер отключается.")
            break

        server_socket.sendto(message, client_address)

    server_socket.close()
    print("Сервер завершил работу.")

if __name__ == '__main__':
    udp_server()
