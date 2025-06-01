import socket
from common import generate_keys, serialize_public_key, deserialize_public_key, derive_key, encrypt_message

def start_client():
    private_key, public_key = generate_keys()

    client = socket.socket()
    client.connect(('localhost', 9000))

    server_key_bytes = b''
    while not server_key_bytes.endswith(b'-----END PUBLIC KEY-----\n'):
        server_key_bytes += client.recv(1024)
    server_public_key = deserialize_public_key(server_key_bytes)

    client.sendall(serialize_public_key(public_key))

    key = derive_key(private_key, server_public_key)

    message = input("Введите сообщение для отправки: ")
    encrypted = encrypt_message(key, message)
    client.sendall(encrypted)

    client.close()

if __name__ == '__main__':
    start_client()
