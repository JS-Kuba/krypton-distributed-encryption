from tkinter import filedialog
from Crypto.Cipher import ARC4
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from os import urandom

class FileEncryptor:
    key = b'my secret key' 

    def get_bytes(self, text, encoding="utf-8"):
        return len(text.encode(encoding))
    
    def split_file_to_list(self, file_path, block_size=1024):
        if not os.path.isfile(file_path):
            print(f"Error: File not found in path {file_path}.")
            return

        blocks = []
        with open(file_path, "r", encoding="utf-8") as input_file:
            block_index = 0
            block_data = ""
            total_bytes = 0

            for line in input_file:
                line_bytes = self.get_bytes(line)
                total_bytes += line_bytes

                if total_bytes >= block_size:
                    block_dict = {"index": block_index, "data": block_data}
                    blocks.append(block_dict)
                    #print(f"Created block {block_index}")
                    block_index += 1

                    block_data = line
                    total_bytes = line_bytes
                else:
                    block_data += line

            if block_data:
                block_dict = {"index": block_index, "data": block_data}
                blocks.append(block_dict)
            print(f"Created blocks: {len(blocks)}")
        return blocks
    
    def encrypt_block(self, block):
        salt = urandom(16)
        password = b"password"

        # Set up Scrypt with high parameters for slow key derivation
        kdf = Scrypt(salt=salt, length=32, n=2**20, r=6, p=6)

        # Derive a key from the password
        key = kdf.derive(password)

        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()

        # Pad the data to a multiple of the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(block['data'].encode('utf-8')) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return (block['index'], ciphertext, key)

    def encrypt_file(self, file_path):
        cipher = ARC4.new(self.key)
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext

    def process_file(self):
        file_path = filedialog.askopenfilename()
        dir_path = os.path.dirname(file_path)
        encrypted_file_path = os.path.join(dir_path, 'encrypted.txt')

        ciphertext = self.encrypt_file(file_path)
        with open(encrypted_file_path, 'wb') as f:
            f.write(ciphertext)

    def decrypt_block(self, block):
        # Now to decrypt
        cipher = Cipher(algorithms.AES(block[2]), modes.ECB())
        decryptor = cipher.decryptor()

        # Decrypt the data
        padded_data = decryptor.update(block[1]) + decryptor.finalize()

        # Unpad the data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        return (block[0], data)
