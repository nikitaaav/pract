from cryptography.fernet import Fernet

def load_key(path="key.key"):
    with open(path, 'rb') as f:
        return f.read()

def decrypt_file(input_path, output_path):
    key = load_key()
    cipher = Fernet(key)

    with open(input_path, 'rb') as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    with open(output_path, 'wb') as f:
        f.write(decrypted)
    print(f"Файл {input_path} расшифрован и сохранён как {output_path}")

if __name__ == '__main__':
    decrypt_file("example.txt.enc", "example_restored.txt")
