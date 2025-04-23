import pygame, components, os
pygame.init()

webcam_path = os.path.join("Assets", "Sprites", "UI", "webcam.png")

class Webcam:
    def __init__(self, position, group=None):

        if group is not None:
            group.append(self)

        self.WIDTH = 350 # PLease
        self.HEIGHT = 350
        self.STIMULUS_WINDOW_WIDTH = 200
        self.position = (position[0] - (self.WIDTH + self.STIMULUS_WINDOW_WIDTH) / 2, position[1])

        self.body = components.generate_window(self.WIDTH, self.HEIGHT, "webcam", color=(0, 0, 0))
        self.display = WebcamDisplay()
        self.stimulus_window = components.generate_window(self.STIMULUS_WINDOW_WIDTH, self.HEIGHT, "prompt")
        self.soup = []

        self.audio_selector = components.Dropdown(
            ["Bird Chirp",
             "Knocking",
             "Baby Crying",
             "Wind",
             "Water Drip",
             "Screaming",
             "Glass Break"],
            (5 + self.WIDTH, 50),
            group=self.soup
        )
        self.video_selector = components.Dropdown(
            ["Mirror",
             "Family Picture",
             "Drawing",
             "Sky",
             "Colored Lights",
             "Lights Off",
             "Flashing Lights"],
            (5 + self.WIDTH, 140),
            group=self.soup
        )
        self.subtitles = components.SubtitleHolder(do_truncation=False)

        self.subtitles.add_subtitle("chicken jockey!", 4, 1)
        self.subtitles.add_subtitle("higher priority subtitle", 2, 2)

        self._build_display()

    def _build_display(self):
        components.TF_BASIC.render_to(self.stimulus_window, (5, 30), "SELECT AUDIO PROMPT")
        components.TF_BASIC.render_to(self.stimulus_window, (5, 110), "SELECT VIDEO PROMPT")

    def render(self, window):

        to_render = pygame.Surface((self.WIDTH + self.STIMULUS_WINDOW_WIDTH, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        to_render.blit(self.display.body, (13, 33))
        to_render.blit(self.stimulus_window, (self.WIDTH, 0))
        self.subtitles.render(to_render, self.WIDTH / 2, 260)
        window.blit(to_render, self.position)
        self.audio_selector.render(window, self.position)

    def mouse_click_behavior(self, x, y):
        for clickable in self.soup:
            clickable.mouse_click_behavior(x, y, self.position)

class WebcamDisplay:
    def __init__(self):
        self.body = pygame.image.load(webcam_path)
