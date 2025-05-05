#the grink
#grython

#import neccessary libraries
import pygame
import json
import os
import random

#open and load file data for the goobers
with open("AnomalyData.json") as file:
    anomaly_data = json.load(file)

with open("BehaviorData.json") as file:
    behavior_data = json.load(file)


pygame.init()

#make a list of names for the possible goobers
names = ["grog", "greg heffley", "gregg gregffley"]


#function to make a random goober
def random_goober(window):
    goober_type = random.choice(list(anomaly_data.keys()))
    goober_name = random.choice(names)
    goober = Goober(window, goober_name, goober_type, (330, 70))
    print(goober_name,goober_type,goober)
    return goober



#Make the Goober class
class Goober:

    #initialize
    def __init__(self, window, name, specific_type, position ):
        #set up the attributes for the goober
        self.type_name = specific_type
        self.specific_type = anomaly_data[specific_type]
        self.behavior = self.specific_type["Behavior"]
        self.name = name
        self.position = position

        print(self.behavior)

        #set up the sprite
        self.sprite = pygame.image.load(os.path.join("Assets", "Sprites", "Goober", self.specific_type["Sprite"]))
        self.sprite = pygame.transform.scale(self.sprite, self.specific_type["Size"])

        #set up the responses based on the behavior
        self.responses = behavior_data[self.behavior]
        self.solution = self.specific_type["Solution"]

        self.window = window
