import socket
import threading

HOST = "0.0.0.0" # Listen on all available network interfaces
PORT = 5000  # Port number match the clint for the TCP connection

# Create a TCP socket using IPv4 and TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port number
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()

# variables to track active clients safely
active_clients = 0
clients_lock = threading.Lock()


def handle_client(conn, addr):
    global active_clients

    # Increment active client count safely using a lock
    with clients_lock:
        active_clients += 1
        print(f" • New client {addr[0]}:{addr[1]} | Active clients: {active_clients}\n")

    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)

            # If no data is received, the client disconnected
            if not data:
                print(f" • Client {addr} closed the connection.")
                break
            # Decode the message
            message = data.decode().strip()
            print(f" From[{addr}] Received: {message}\n")

            # If client requests to terminate the connection
            if message.lower() == "finish":
                print(f" • Client {addr} requested to close the connection with FINISH.")
                break

            try:
                # Split the received message into base and exponent
                base_str, exp_str = message.split("^")

                # Convert input values to integers
                base = int(base_str)
                exponent = int(exp_str)

                # Prepare the response
                result = base ** exponent
                response = f"{base}^{exponent} = {result}"

            except Exception:
                # Handle invalid input format
                response = " x ERROR: send as: base^exponent (e.g., 3^5)"

            # Send the response back to the client
            conn.sendall(response.encode())

    finally:
        # Close the connection and update client count
        conn.close()
        with clients_lock:
            active_clients -= 1
            print(f" • Connection with {addr} closed. Active clients: {active_clients}")


def main():
    print(f" [SERVER] Listening on {HOST}:{PORT} ...\n")

    while True:
        print(" [SERVER] Waiting for a client...\n")
        # Accept a new client connection
        conn, addr = server_socket.accept()
        print(f" + Client connected from {addr}\n")

        # Create a new thread for each connected client
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        client_thread.start()


if __name__ == "__main__":
    main()
