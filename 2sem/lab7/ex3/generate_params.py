from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Генерация параметров DH
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

# Сохраняем в файл
with open("dh_params.pem", "wb") as f:
    f.write(parameters.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    ))

print("Параметры сохранены в dh_params.pem")
