from tkinter import filedialog
from Crypto.Cipher import ARC4
import os

class FileEncryptor:
    key = b'my secret key' 

    def get_bytes(self, text, encoding="utf-8"):
        return len(text.encode(encoding))

    def split_file_to_list(self, file_path, block_size=500 * 1024):
        if not os.path.isfile(file_path):
            print("Error: File not found.")
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
                #print(f"Created block {block_index}")
        return blocks
    
    def encrypt_block(self, block):
        cipher = ARC4.new(self.key)
        ciphertext = cipher.encrypt(block)
        return ciphertext

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
