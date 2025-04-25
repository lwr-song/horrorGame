#the grink
#grython
import pygame
import json
import os
import components
import random

types = ["Shminguss", "Yargle Bargle", "Dingus", "Tinky Winky", "OOOOOh"]
behaviors = ["aggressive", "docile", "silent", "stubborn"]

with open("AnomalyData.json") as file:
    anomaly_data = json.load(file)

with open("BehaviorData.json") as file:
    behavior_data = json.load(file)


pygame.init()


names = ["grog", "greg heffley", "gregg gregffley"]

def random_goober(window):
    goober_type = random.choice(list(anomaly_data.keys()))
    goober_name = random.choice(names)
    goober = Goober(window, goober_name, goober_type)
    return goober

#grorganization
#solution = "Shminguss" (specific type)
#behavior example:
#docile = [Visual, Audio, Interaction]
#Visual = {"Mirror": 5, "Picture": 5, "Drawing": 90,  "Sky": 80, "Color":70, "LightsOff":5, "FlashingLights": 10}
#size = (width, height)
#

class Goober:

    def __init__(self, window, name, specific_type, position ):
        self.specific_type = anomaly_data[specific_type]
        self.behavior = self.specific_type["Behavior"]
        self.name = name
        self.position = position

        self.sprite = pygame.image.load( os.path.join("Assets","Sprites","Goober", self.specific_type["Sprite"] ))

        self.sprite = pygame.transform.scale(self.sprite, self.specific_type["Size"])


        self.responses = behavior_data[self.behavior]
        self.solution = self.specific_type["Solution"]



        self.window = window
        window.blit(self.sprite, position)


   # def hovered(self, window, mouse_pos):
       # position = pygame.mouse.get_pos()
       # if mouse_pos.

