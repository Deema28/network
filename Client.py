import socket
import time


# Server Configuration
HOST = "172.20.10.2"  # Server IP address
PORT = 5000 # Port number match the Server for the TCP connection

def main():
    # Create a TCP socket using IPv4 and TCP protocol
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to server {HOST}:{PORT}")

    while True:
        # Take user input in the format(base^exponent)
        user_input = input("Enter expression (format: base^exponent), or type 'Finish' to exit: ").strip()

        # Handle empty input
        if not user_input:
            continue

        # If user wants to terminate the connection
        if user_input.lower() == "finish":
            client_socket.sendall(user_input.encode()) 
            print("[CLIENT] Closing connection...")
            break
    
        # Record start time before sending the request
        start_time = time.time()

        # Send the input data to the server
        client_socket.sendall(user_input.encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode().strip()

        # Record end time after receiving the response
        end_time = time.time()

        # Calculate Round-Trip Time (RTT) in milliseconds
        rtt_ms = (end_time - start_time) * 1000
    
        # Display the result and RTT
        print(f"Result from server: {response}  |  RTT: {rtt_ms:.3f} ms\n")

    # Close the socket connection
    client_socket.close()
    print("[CLIENT] Connection closed.")


if __name__ == "__main__":
    main()
