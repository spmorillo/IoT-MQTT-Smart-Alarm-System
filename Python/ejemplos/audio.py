import pygame
import time
pygame.mixer.init()
pygame.mixer.music.load("correct_code.mp3")
#pygame.mixer.music.load("error.mp3")
#pygame.mixer.music.load("Siren.mp3")
#pygame.mixer.music.load("welcome.mp3")
i=0
while(True):
   pygame.mixer.music.play(loops=3)