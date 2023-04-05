import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import ARC4

def encrypt_file(file_path):
    key = b'my secret key' 
    cipher = ARC4.new(key)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def process_file():
    file_path = filedialog.askopenfilename()
    ciphertext = encrypt_file(file_path)
    with open('encrypted.txt', 'wb') as f:
        f.write(ciphertext)


root = tk.Tk()
root.geometry('500x300')
root.title('File Processor')

drop_label = tk.Label(root, text='Drop a file here')
drop_label.pack(pady=50)

# result_label = tk.Label(root, text='')
# result_label.pack(pady=20)

root.bind('<Button-1>', lambda e: process_file())

root.mainloop()
