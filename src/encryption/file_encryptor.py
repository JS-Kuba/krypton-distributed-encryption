import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

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
                    block_tuple = (block_index, block_data)
                    blocks.append(block_tuple)
                    block_index += 1

                    block_data = line
                    total_bytes = line_bytes
                else:
                    block_data += line

            if block_data:
                block_tuple = (block_index, block_data)
                blocks.append(block_tuple)
            print(f"Created blocks: {len(blocks)}")
        return blocks