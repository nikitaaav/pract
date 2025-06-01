from cryptography.fernet import Fernet

def load_key(path="key.key"):
    with open(path, 'rb') as f:
        return f.read()

def encrypt_and_save(message, output_file):
    key = load_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print(f"Сообщение зашифровано и сохранено в {output_file}")

if __name__ == '__main__':
    msg = input("Введите сообщение для шифрования: ")
    encrypt_and_save(msg, "encrypted_message.txt")
