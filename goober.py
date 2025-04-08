#the grink
#grython
import pygame
pygame.init()

behaviors = ["aggressive", "docile", "silent", "stubborn"]
names = ["grog", "greg heffley"]

class Goober:

    def __init__(self, window, name, size, sprite, behavior, solution):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.responses = self.determine_responses()
        self.solution = solution


    def determine_responses(self):
        return "aaa"

