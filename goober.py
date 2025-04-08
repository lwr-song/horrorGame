#the grink
#grython
import pygame
pygame.init()

_behaviors = ["aggressive", "docile", "silent", "stubborn"]
names = ["grog", "greg heffley"]
types = ["bigfoot", "greg heffley's foot", "greg heffley", "athlete's foot"]

class Goober:

    def __init__(self, window, name, size, sprite, behavior, erratic, solution):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.responses = {}
        self.solution = solution
        self.behavior = behavior
        self.erratic = erratic



    def determine_responses(self):
        if self.behavior in _behaviors:
            return {"Visual":"Lights", }

entity = Goober