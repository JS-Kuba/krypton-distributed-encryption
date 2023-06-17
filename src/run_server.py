import socket
import threading
import subprocess
import re
import os
import queue
import time
import ast

from encryption.file_encryptor import FileEncryptor

class Server:


    def __init__(self):
        self.PORT = 12345
        self.BUFFER_SIZE = 7024
        self.clients = []
        self.client_threads = []
        self.decryption_threads = []
        #self.IPv4 = self.obtain_ipv4()
        self.IPv4 = '127.0.0.1'
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(os.path.dirname(self.current_dir), "data")
        self.results_queue = queue.Queue()
        self.sorted_queue = queue.Queue()
        self.decrypted_queue = queue.Queue()

    def run_encryption(self):
        for thread in self.client_threads:
            thread.start()
        # czy to jest konieczne skoro będzie jeszcze odszyfrowanie?
        for thread in self.client_threads:
            thread.join()
        self.sorted_queue = self.sort_queue()
        

    def read_block_tuple(self, block_string):
        return ast.literal_eval(block_string)

    def sort_queue(self):
        # Convert the queue to a list
        elements = list(self.results_queue.queue)
        elements_tuples = [self.read_block_tuple(block) for block in elements]

        with open("results_unsorted.txt", 'w') as f:
            for element in elements_tuples:
                f.write(f"index: {element[0]}\nciphertext: {element[1]}\nkey: {element[2]}" + '\n')

        # Sort the list
        sorted_elements = sorted(elements_tuples, key=lambda x: x[0])

        # Create a new queue
        sorted_queue = queue.Queue()

        # Enqueue the sorted elements into the new queue
        with open("results_sorted.txt", 'w') as f:
            for element in sorted_elements:
                sorted_queue.put(element)
                f.write(f"index: {element[0]}\nciphertext: {element[1]}\nkey: {element[2]}" + '\n')

        return sorted_queue


    def obtain_ipv4(self):
        try:
            os_name = os.name
            if os_name == 'nt':
                if os_name == 'nt':
                    # print("Recognized operating system: Windows")
                    # command = 'ipconfig | findstr IPv4'
                    # output = subprocess.check_output(command, shell=True, encoding='utf-8')
                    # ip_address = output.split(':')[-1].strip()
                    # print(f"Obtained IP: {ip_address}")
                    ip_address = "127.0.0.1"
                    return ip_address

            elif os_name == 'posix':
                print("Recognized operating system: Linux")
                output = subprocess.check_output("ip route get 8.8.8.8 | awk 'NR==1 {print $NF; exit}'", shell=True)
                ipv4_addresses = re.findall(r'(\d+\.\d+\.\d+\.\d+)', output)
                print(f"Obtained IP: {ipv4_addresses}")
                return(output)
            
            else:
                print("Unknown operating system")

        except Exception as e:
            print("Could not find IPv4 address:", e)

    def handle_client(self, client_socket, client_address, input_queue, results_queue):
        """
        Thread function to handle each client connection
        """
        print("I am ready to work!")
        worker_available = True
        waiting_for_response = False
        try:
            while not input_queue.empty():
                if worker_available:
                    print(f"Fetching a block from the queue... {input_queue.qsize()} items left to distribute")
                    block = input_queue.get()
                    block_index = block['index']
                    block_data = block['data']
                    block_tuple = (block_index, block_data)

                    print("Block fetched. Preparing for sending...")
                    try:
                        # sending data to the worker client
                        client_socket.sendall(str(block_tuple).encode("utf-8"))
                        worker_available = False
                        print("Block sent. Waiting for response.")
                    except Exception as e:
                        print(f"Error occurred while sending: {str(e)}")
                    waiting_for_response = True
                while waiting_for_response:
                    try:
                        # Receive message from client
                        data = client_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                        if data:
                            print(f'Received from {client_address}: {data}')
                            results_queue.put(data)

                            worker_available = True
                            waiting_for_response = False
                        else:
                            # --------------------------
                            # TUTAJ DO POPRAWY
                            # If data is empty, the client has closed the connection
                            time.sleep(2)
                            print("Data received from client is empty. Removing client.")
                            self.remove_client(client_socket)
                            break
                    except Exception as e:
                        print(f'Error: {e}')
                        self.remove_client(client_socket)
                        break
            print(f"Queue size: {input_queue.qsize()}. Worker finished encoding.")

        except Exception as e:
            print(f"Error in sending message to the client: {e}")
            client_socket.close()
            self.remove_client(client_socket)
            

    def decrypt(self, client_socket, client_address, decrypted_queue):
        pass


    def remove_client(self, client_socket):
        """
        Removes a client from the list of connected clients
        """
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()
    

    def define_job_queue(self):
        fe = FileEncryptor()
        input_file_path = os.path.join(self.data_dir, 'crime-and-punishment.txt')
        blocks_list = fe.split_file_to_list(input_file_path)

        input_queue = queue.Queue()

        # Add the input strings to the queue
        for block in blocks_list:
            input_queue.put(block)
        
        return input_queue


    def start_server(self):
        """
        Starts the server and listens for incoming connections
        """
        input_queue = self.define_job_queue()
        
        
        print(f"Server will be run on: {self.IPv4}")
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.IPv4, self.PORT))
        server_socket.listen(5)
        print(f'Server is running on {self.IPv4}:{self.PORT}')


        
        while True:
            try:
                # Accept client connection
                client_socket, client_address = server_socket.accept()
                print(f'Connected to {client_address}')
                self.clients.append({"client_socket" : client_socket, "client_address" : client_address})

               
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address, input_queue, self.results_queue))
                self.client_threads.append(client_thread)

                decryption_thread = threading.Thread(target=self.decrypt, args=(client_socket, client_address, self.decrypted_queue))
                self.decryption_threads.append(decryption_thread)

            except Exception as e:
                print(f'Error: {e}')
                break
        # Close server socket
        server_socket.close()
