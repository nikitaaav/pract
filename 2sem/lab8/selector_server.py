import selectors
import socket

selector = selectors.DefaultSelector()


def accept(sock):
    conn, addr = sock.accept()
    print(f"╭─ Selector Server ─{'─' * 40}╮")
    print(f"│ New connection from {addr}")
    print(f"╰─{'─' * 60}╯")
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, echo)


def echo(conn):
    try:
        data = conn.recv(1024)
        if data:
            if data.decode().strip().lower() == 'shutdown':
                print("╭─ Selector Server ─{'─' * 40}╮")
                print("│ Shutdown command received")
                print(f"╰─{'─' * 60}╯")
                selector.unregister(conn)
                conn.close()
                raise KeyboardInterrupt
            print("╭─ Selector Server ─{'─' * 40}╮")
            print(f"│ Echo: {data.decode()}")
            print(f"╰─{'─' * 60}╯")
            conn.sendall(data)
        else:
            selector.unregister(conn)
            conn.close()
    except:
        selector.unregister(conn)
        conn.close()


def run_selector_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9093))
    server.listen()
    server.setblocking(False)
    selector.register(server, selectors.EVENT_READ, accept)
    print("╭─ Selector Server ─{'─' * 40}╮")
    print("│ Server started and listening...")
    print(f"╰─{'─' * 60}╯")
    try:
        while True:
            events = selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        print("╭─ Selector Server ─{'─' * 40}╮")
        print("│ Server terminated")
        print(f"╰─{'─' * 60}╯")
