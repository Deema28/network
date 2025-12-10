import socket

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

def main():

 while True :
   print("[SERVER] Waiting for a client...")

   conn, addr = server_socket.accept()
   print(f"[+] Client connected from {addr}")

   while True:
       data = conn.recv(1024).decode().strip()
  
       if not data:
           print("[*] Client closed the connection.")
           break

       
       print("Received:", data)

       if data.lower() == "quit":
           print("[*] Client requested to close the connection.")
           break
       try:
           base_str, exp_str = data.split("-")   
           base =  float(base_str)             
           exponent = float(exp_str)          

           result = base ** exponent          
           response = str(result)         
       except Exception:
           response = "ERROR: send as: base-exponent"

       conn.sendall(response.encode())
   conn.close()
   print("[*] Connection closed.")


if __name__ == "__main__":
    main()