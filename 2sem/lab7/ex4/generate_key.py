from cryptography.fernet import Fernet

def save_key(path="key.key"):
    key = Fernet.generate_key()
    with open(path, 'wb') as f:
        f.write(key)
    print("Секретный ключ сохранён в key.key")

if __name__ == '__main__':
    save_key()
