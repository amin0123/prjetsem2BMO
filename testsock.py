import socket

# Define the IP address and port of the Raspberry Pi server
SERVER_HOST = '192.168.84.170'  # Replace with the Raspberry Pi's IP address
SERVER_PORT = 6060            # Replace with the port you chose on the Raspberry Pi

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    while True:
        # Get user input
        message = input("Enter message to send (or 'quit' to exit): ")
        
        if message.lower() == 'quit':
            break
        
        # Send the message to the server
        client_socket.sendall(message.encode())
