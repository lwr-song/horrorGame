import pygame, components, os
pygame.init()

webcam_path = os.path.join("Assets", "Sprites", "UI", "webcam.png")

class Webcam:
    def __init__(self):

        self.WIDTH = 350 # PLease
        self.HEIGHT = 350

        self.body = components.generate_window(self.WIDTH, self.HEIGHT, "webcam")
        self.display = WebcamDisplay()

        self.audio_selector = components.Dropdown(
            ["Bird chirp",
             "Knocking",
             "Baby cry",
             "Wind",
             "Water drip",
             "Screaming",
             "Glass break"],
            120, (13, 295)
        )

        self._build_display()

    def _build_display(self):
        components.TF_BASIC.render_to(self.body, (13, 270), "SELECT AUDIO PROMPT")

    def render(self, window, position):

        to_render = pygame.Surface((self.WIDTH, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        to_render.blit(self.display.body, (13, 33))

        window.blit(to_render, position)
        self.audio_selector.render(window)

class WebcamDisplay:
    def __init__(self):
        self.body = pygame.image.load(webcam_path)
