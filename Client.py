import socket
import time



HOST = "127.0.0.1"
PORT = 5000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to server {HOST}:{PORT}")

    while True:
        
        user_input = input("Enter expression (format: base^exponent), or type 'Finish' to exit: ").strip()

        if not user_input:
            continue

        
        if user_input.lower() == "finish":
            client_socket.sendall(user_input.encode()) 
            print("[CLIENT] Closing connection...")
            break

      
        start_time = time.time()

        
        client_socket.sendall(user_input.encode())

        
        response = client_socket.recv(1024).decode().strip()

        
        end_time = time.time()
        rtt_ms = (end_time - start_time) * 1000

        print(f"Result from server: {response}  |  RTT: {rtt_ms:.3f} ms")

    client_socket.close()
    print("[CLIENT] Connection closed.")


if __name__ == "__main__":
    main()
