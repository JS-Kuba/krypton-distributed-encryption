import tkinter as tk
from encryption.file_encryptor import FileEncryptor
from utils.music_player import MusicPlayer

file_encryptor = FileEncryptor()

music_player = MusicPlayer(volume=0.3)
music_player.play_music()

# Create the main window
root = tk.Tk()
root.title("Text File Reader")
root.geometry("800x800")
root.title('KRYPTON')

# Set the background image
bg_image = tk.PhotoImage(file="src/assets/krypton1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a menu bar with a "File" menu
menu_bar = tk.Menu(root)

label = tk.Label(root, text="Drag and drop a file here", font='Helvetica 22 bold', padx='10px', pady='10px')
label.place(rely=0.5, relx=0.27)
label.bind("<Button-1>", lambda e: file_encryptor.process_file())

# Run the main loop
root.mainloop()
