import socket
from common import generate_keys, serialize_public_key, deserialize_public_key, derive_key, decrypt_message

def start_server():
    private_key, public_key = generate_keys()

    server = socket.socket()
    server.bind(('localhost', 9000))
    server.listen(1)
    print("Ожидание клиента...")

    conn, addr = server.accept()
    print(f"Подключён клиент: {addr}")

    conn.sendall(serialize_public_key(public_key))

    client_key_bytes = b''
    while not client_key_bytes.endswith(b'-----END PUBLIC KEY-----\n'):
        client_key_bytes += conn.recv(1024)
    client_public_key = deserialize_public_key(client_key_bytes)

    key = derive_key(private_key, client_public_key)

    encrypted = conn.recv(4096)
    message = decrypt_message(key, encrypted)
    print("Получено сообщение:", message.decode())

    conn.close()
    server.close()

if __name__ == '__main__':
    start_server()
