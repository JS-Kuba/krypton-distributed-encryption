from tkinter import filedialog
from Crypto.Cipher import ARC4
import os

class FileEncryptor:
    key = b'my secret key' 

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
