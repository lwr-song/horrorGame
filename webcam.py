import pygame, components, os
pygame.init()

class Webcam:
    def __init__(self):

        self.WIDTH = 300 # PLease
        self.HEIGHT = 200

        self.body = components.generate_window(self.WIDTH, self.HEIGHT, "webcam")

    def render(self, window):

        window.blit(self.body, (window.get_width() / 2 - self.WIDTH / 2,
                           200))
