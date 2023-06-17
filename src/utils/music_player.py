import pygame

class MusicPlayer:
    def __init__(self, volume) -> None:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)

    def play_music(self):
        pygame.mixer.music.load("assets/levo.mp3")
        pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        pygame.mixer.music.stop()