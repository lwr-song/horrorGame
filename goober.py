#the grink
#grython
import pygame
pygame.init()

behaviors = ["aggressive", "docile"]
names = ["grog", "greg heffley"]

class Goober:

    def __init__(self, window, name, size, sprite, behavior, responses):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.responses = self.determine_responses()
        window.blit(self.sprite, (100,200))

    def determine_responses(self):
        return "aaa"

