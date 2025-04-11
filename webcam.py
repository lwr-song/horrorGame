import pygame, graphical, os
pygame.init()

class Webcam:
    def __init__(self):

        self.WIDTH = 300 # PLease
        self.HEIGHT = 200

        self.body = graphical.generate_window(self.WIDTH, self.HEIGHT, "webcam")

