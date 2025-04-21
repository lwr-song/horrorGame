import pygame, components, os
pygame.init()

webcam_path = os.path.join("Assets", "Sprites", "UI", "webcam.png")

class Webcam:
    def __init__(self):

        self.WIDTH = 350 # PLease
        self.HEIGHT = 270

        self.body = components.generate_window(self.WIDTH, self.HEIGHT, "webcam")
        self.display = WebcamDisplay()

    def render(self, window, position):

        to_render = pygame.Surface((self.WIDTH, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        to_render.blit(self.display.body, (13, 33))

        window.blit(to_render, position)

class WebcamDisplay:
    def __init__(self):
        self.body = pygame.image.load(webcam_path)
