import socket

host = 'google.com'
port = 80

request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    s.sendall(request.encode())

    response = ""
    while True:
        part = s.recv(4096).decode()
        if not part:
            break
        response += part

headers, _, body = response.partition('\r\n\r\n')
status_line = headers.splitlines()[0]
status_code = status_line.split(' ')[1]

print(f"Статус-код: {status_code}")
print("Заголовки ответа:")
print('\n'.join(headers.splitlines()[1:]))
