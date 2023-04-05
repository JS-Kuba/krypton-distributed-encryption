import tkinter as tk
from tkinter import font, filedialog
import pygame

def play_music():
    pygame.mixer.music.load("assets\\levo.mp3")
    pygame.mixer.music.play(loops=-1)

def stop_music():
    pygame.mixer.music.stop()


# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)
play_music()


# Create the main window
root = tk.Tk()
root.title("Text File Reader")
root.geometry("800x800")
root.title('KRYPTON')

# Set the background image
bg_image = tk.PhotoImage(file="assets\\krypton1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)


def drop_file():
    file_path = filedialog.askopenfilename()
    # Do something with the selected file path, such as print it
    print("Selected file path:", file_path)

# Create a menu bar with a "File" menu
menu_bar = tk.Menu(root)


label = tk.Label(root, text="Drag and drop a file here", font='Helvetica 22 bold', padx='10px', pady='10px')
label.place(rely=0.5, relx=0.27)
label.bind("<Button-1>", lambda e: drop_file())


# Run the main loop
root.mainloop()
