from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

def load_parameters():
    with open("dh_params.pem", "rb") as f:
        return serialization.load_pem_parameters(f.read(), backend=default_backend())

def generate_keys():
    parameters = load_parameters()
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(peer_bytes):
    return serialization.load_pem_public_key(peer_bytes, backend=default_backend())

def derive_key(private_key, peer_public_key):
    shared_secret = private_key.exchange(peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake',
        backend=default_backend()
    ).derive(shared_secret)

def encrypt_message(key, message):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(message.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext

def decrypt_message(key, data):
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded) + unpadder.finalize()
