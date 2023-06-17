import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024    # Buffer size for receiving messages

# List to store all connected clients
clients = []

def handle_client(client_socket, client_address):
    """
    Thread function to handle each client connection
    """
    try:
        client_socket.sendall('{"index": 1, "data": "Hello World!"}'.encode("utf-8"))
    except Exception as e:
        print(f"Error in sending message to the client: {e}")
        client_socket.close()
        remove_client(client_socket)

    while True:
        try:
            # Receive message from client
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if data:
                print(f'Received from {client_address}: {data}')
            else:
                # If data is empty, the client has closed the connection
                remove_client(client_socket)
                break
        except Exception as e:
            print(f'Error: {e}')
            remove_client(client_socket)
            break


def remove_client(client_socket):
    """
    Removes a client from the list of connected clients
    """
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    """
    Starts the server and listens for incoming connections
    """
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Server is running on {HOST}:{PORT}')

    while True:
        try:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            print(f'Connected to {client_address}')
            clients.append(client_socket)

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except Exception as e:
            print(f'Error: {e}')
            break

    # Close server socket
    server_socket.close()

if __name__ == '__main__':
    start_server()