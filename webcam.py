import pygame, components, os, goober, goober_selector
pygame.init()

WEBCAM_PATH = os.path.join("Assets", "Sprites", "UI", "webcam.png")
WEBCAM_SIZE = (650, 420)

class Webcam:
    def __init__(self, position, window, group=None):

        # The Webcam has clickable components, so it needs to be in a group (Soup)
        if group is not None:
            group.append(self)

        self.WIDTH = 700 # PLease
        self.HEIGHT = 430
        self.STIMULUS_WINDOW_WIDTH = 200
        self.position = (position[0] - (self.WIDTH + self.STIMULUS_WINDOW_WIDTH) / 2, position[1])

        self.body = components.generate_window_sprite(self.WIDTH, self.HEIGHT, "webcam", color=(0, 0, 0))
        self.stimulus_window = components.generate_window_sprite(self.STIMULUS_WINDOW_WIDTH, self.HEIGHT, "prompt")
        self.soup = []

        # Dropdown for selecting an audio stimulus
        self.audio_selector = components.Dropdown(
            ["Bird Chirp",
             "Knocking",
             "Baby Crying",
             "Wind",
             "Water Drip",
             "Screaming",
             "Glass Break"],
            (5 + self.WIDTH, 60),
            self.STIMULUS_WINDOW_WIDTH - 10,
            group=self.soup
        )

        # Dropdown for selecting a visual stimulus
        self.video_selector = components.Dropdown(
            ["Mirror",
             "Family Picture",
             "Drawing",
             "Sky",
             "Colored Lights",
             "Lights Off",
             "Flashing Lights"],
            (5 + self.WIDTH, 140),
            self.STIMULUS_WINDOW_WIDTH - 10,
            group=self.soup
        )

        # Subtitle holder
        self.subtitles = components.SubtitleHolder(2, do_truncation=False)

        # Button for submitting audio stumulus
        self.submit_audio_button = components.Button(
            self.WIDTH + 5,
            self.HEIGHT - 100,
            self.STIMULUS_WINDOW_WIDTH - 10,
            35,
            "submit_audio",
            "Play Audio",
            group=self.soup
        )

        # Button for submitting visual stimulus
        self.submit_video_button = components.Button(
            self.WIDTH + 5,
            self.HEIGHT - 50,
            self.STIMULUS_WINDOW_WIDTH - 10,
            35,
            "submit_video",
            "Play Video",
            group=self.soup
        )

        self.anomaly_selector = goober_selector.GooberSelector(self.soup)

        self.display = WebcamDisplay(window)
        self._build_display()

    def _build_display(self):

        # Furnishes the window with text and the like
        # Just to avoid overcrowding
        components.TF_BASIC.render_to(self.stimulus_window, (5, 30), "Select Audio Prompt")
        components.TF_BASIC.render_to(self.stimulus_window, (5, 110), "Select Video Prompt")

    def render(self, window):

        to_render = pygame.Surface((self.WIDTH + self.STIMULUS_WINDOW_WIDTH, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        #self.display.render((13, 13), self.position)
        to_render.blit(self.display.body, (13, 33))
        to_render.blit(self.stimulus_window, (self.WIDTH, 0))
        self.subtitles.render(to_render, self.WIDTH / 2, 380)

        self.submit_audio_button.render(to_render)
        self.submit_video_button.render(to_render)

        window.blit(to_render, self.position)

        self.video_selector.render(window, self.position)
        self.audio_selector.render(window, self.position)

        self.anomaly_selector.render(window)

        self.display.load_goober(window)

    def mouse_click_behavior(self, x, y):
        for clickable in self.soup:
            response = clickable.mouse_click_behavior(x, y, self.position)

            match response:
                case "submit_video":
                    print(self.video_selector.selection)
                case "submit_audio":
                    audio_selection = self.audio_selector.selection
                    self.subtitles.add_subtitle("(" + audio_selection[0] + audio_selection[1:].lower() + ")", 3, 0)

                    print(self.display.active_goober.responses['Sound'][audio_selection])

            if response is not None:
                return True

# TODO: make window uh bigger :D yayyy yayyy ya y ay yyy
class WebcamDisplay:
    def __init__(self,window):
        self.body = pygame.image.load(WEBCAM_PATH)
        self.body = pygame.transform.scale(self.body, WEBCAM_SIZE)
        self.active_goober = None
        self.active_goober = goober.random_goober(window)


        self.load_goober(window)

    def load_goober(self,window):

        window.blit(self.active_goober.sprite, self.active_goober.position )
"""
    def render(self, x, y, relative_position=(0,0)):
        x += relative_position[0]
        y += relative_position[1]

        to_render = pygame.Surface(WEBCAM_SIZE)
        to_render.blit(self.body, (0, 0))
        to_render.blit(self.active_goober.sprite, (0, 0))

        
        self.active_goober.render()
"""