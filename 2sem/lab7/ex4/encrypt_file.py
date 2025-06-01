from cryptography.fernet import Fernet

def load_key(path="key.key"):
    with open(path, 'rb') as f:
        return f.read()

def encrypt_file(input_path, output_path):
    key = load_key()
    cipher = Fernet(key)

    with open(input_path, 'rb') as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    with open(output_path, 'wb') as f:
        f.write(encrypted)
    print(f"Файл {input_path} зашифрован и сохранён как {output_path}")

if __name__ == '__main__':
    encrypt_file("example.txt", "example.txt.enc")
