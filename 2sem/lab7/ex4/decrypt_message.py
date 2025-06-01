from cryptography.fernet import Fernet, InvalidToken

def load_key(path="key.key"):
    with open(path, 'rb') as f:
        return f.read()

def decrypt_from_file(input_file):
    key = load_key()
    cipher = Fernet(key)

    with open(input_file, 'rb') as f:
        encrypted = f.read()

    try:
        decrypted = cipher.decrypt(encrypted)
        print("Расшифрованное сообщение:", decrypted.decode())
    except InvalidToken:
        print("Ошибка: неверный ключ или повреждённое сообщение!")
    except Exception as e:
        print("Не удалось расшифровать:", str(e))

if __name__ == '__main__':
    decrypt_from_file("encrypted_message.txt")
