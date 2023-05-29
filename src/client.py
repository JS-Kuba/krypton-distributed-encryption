import socket
import threading
import ast
import subprocess

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from os import urandom

HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1064

# Use the subprocess module to install required module
# try:
#     subprocess.check_call(["pip", "install", "cryptography"])
#     print(f"Successfully installed cryptography")
# except subprocess.CalledProcessError:
#     print(f"Failed to install cryptography")



class BlockEncryptor:

    def read_block_tuple(self, block_string):
        return ast.literal_eval(block_string)


    def encrypt_block(self, block):
        salt = urandom(16)
        password = b"password"

        block_tuple = self.read_block_tuple(block_string=block)
        block_index = block_tuple[0]
        block_text = block_tuple[1]

        # Set up Scrypt with high parameters for slow key derivation
        kdf = Scrypt(salt=salt, length=32, n=2**10, r=6, p=6)

        # Derive a key from the password
        key = kdf.derive(password)

        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()

        # Pad the data to a multiple of the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(block_text.encode('utf-8')) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return (block_index, ciphertext, key)

    
    def decrypt_block(self, block):
        # Now to decrypt
        cipher = Cipher(algorithms.AES(block['key']), modes.ECB())
        decryptor = cipher.decryptor()

        # Decrypt the data
        padded_data = decryptor.update(block['ciphertext']) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return (block['index'], data)
    
class Worker:
    
    def __init__(self) -> None:
        self.be = BlockEncryptor()

    def handle_received_blocks(self, client_socket):
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8')

                if data:
                    block = data
                    print(f"Worker received: {block}")
                    encrypted_block = self.be.encrypt_block(block)
                    print(f"Worker encrypted the block: {encrypted_block}")
                    client_socket.sendall(str(encrypted_block).encode('utf-8'))
                else:
                    print("Closing client socket.")
                    client_socket.close()
                    break
            except Exception as e:
                print(f'Error: {e}')
                client_socket.close()
                break


    def start_worker(self):
        """Start the worker client and connect to the server."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')

        receive_thread = threading.Thread(target=self.handle_received_blocks, args=(client_socket,))
        receive_thread.start()

worker = Worker()
worker.start_worker()
