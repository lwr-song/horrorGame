#the grink
#grython
import pygame
import csv


types = ["Shminguss", "Yargle Bargle", "Dingus", "Tinky Winky", "OOOOOh"]
_behaviors = ["aggressive", "docile", "silent", "stubborn"]
rows = []
with open("AnomalyData.csv") as csv_file:
    reader = csv.DictReader(csv_file, fieldnames = _behaviors)
    for row in reader:
        rows.append(row)

pygame.init()


names = ["grog", "greg heffley"]

#grorganization
#solution = "Shminguss" (specific type)
#behavior example:
#docile = [Visual, Audio, Interaction]
#Visual = {"Mirror": 5, "Picture": 5, "Drawing": 90,  "Sky": 80, "Color":70, "LightsOff":5, "FlashingLights": 10}
#
#
class Goober:

    def __init__(self, window, name, size, sprite, behavior, solution):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.sprite.size = size

        self.responses = {}
        self.solution = solution
        self.behavior = behavior
        self.window = window


    def determine_responses(self):
        print("AA")

