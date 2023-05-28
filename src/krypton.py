import tkinter as tk
from encryption.file_encryptor import FileEncryptor
from utils.music_player import MusicPlayer
from run_server import Server
import threading

def start_server_thread(event, server):
    # Create and start the server instance on a new thread
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()

def run_encryption():
    server.run_encryption()

file_encryptor = FileEncryptor()
server = Server()

music_player = MusicPlayer(volume=0.3)
music_player.play_music()

# Create the main window
root = tk.Tk()
root.title("Text File Reader")
root.geometry("800x800")
root.title('KRYPTON')
root.resizable(False, False)


# Set the background image
bg_image = tk.PhotoImage(file="assets/krypton1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a menu bar with a "File" menu
menu_bar = tk.Menu(root)

server_start_btn = tk.Button(root, text="Start server", font='Helvetica 22 bold', padx='10px', pady='10px')
server_start_btn.place(rely=0.5, relx=0.27)
server_start_btn.bind("<Button-1>", lambda e: start_server_thread(e, server))

run_btn = tk.Button(root, text="Run", font='Helvetica 22 bold', padx='10px', pady='10px')
run_btn.place(rely=0.7, relx=0.27)
run_btn.bind("<Button-1>", lambda e: run_encryption())

# Run the main loop
root.mainloop()
