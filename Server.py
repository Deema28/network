import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

active_clients = 0
clients_lock = threading.Lock()


def handle_client(conn, addr):
    global active_clients

    with clients_lock:
        active_clients += 1
        print(f" • New client {addr[0]}:{addr[1]} | Active clients: {active_clients}\n")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f" • Client {addr} closed the connection.")
                break

            message = data.decode().strip()
            print(f" From[{addr}] Received: {message}\n")

           
            if message.lower() == "finish":
                print(f" • Client {addr} requested to close the connection with FINISH.")
                break

            try:
                base_str, exp_str = message.split("^")

                base = int(base_str)
                exponent = int(exp_str)

                result = base ** exponent
                response = f"{base}^{exponent} = {result}"

            except Exception:
                response = " x ERROR: send as: base^exponent (e.g., 3^5)"

            conn.sendall(response.encode())

    finally:
        conn.close()
        with clients_lock:
            active_clients -= 1
            print(f" • Connection with {addr} closed. Active clients: {active_clients}")


def main():
    print(f" [SERVER] Listening on {HOST}:{PORT} ...\n")

    while True:
        print(" [SERVER] Waiting for a client...\n")
        conn, addr = server_socket.accept()
        print(f" + Client connected from {addr}\n")

        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        client_thread.start()


if __name__ == "__main__":
    main()
