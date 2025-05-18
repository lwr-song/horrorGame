import pygame, components, os, goober, goober_selector, time, random, math
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
        self.audio_playable_timestamp = -1

        self.anomaly_selector = goober_selector.GooberSelector(self.soup)

        self.display = WebcamDisplay(window)
        self._build_display()

    def _build_display(self):

        # Furnishes the window with text and the like
        # Just to avoid overcrowding
        components.TF_BASIC.render_to(self.stimulus_window, (5, 30), "Select Audio Prompt")
        components.TF_BASIC.render_to(self.stimulus_window, (5, 110), "Select Video Prompt")
    
    def update_button_statuses(self):
        if time.time() > self.audio_playable_timestamp:
            if self.submit_audio_button.text != "Play Audio":
                self.submit_audio_button.change_text("Play Audio")

    def render(self, window):

        self.update_button_statuses()

        to_render = pygame.Surface((self.WIDTH + self.STIMULUS_WINDOW_WIDTH, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        #self.display.render((13, 13), self.position)
        self.display.render(13, 33, to_render)
        to_render.blit(self.stimulus_window, (self.WIDTH, 0))

        self.submit_audio_button.render(to_render)
        self.submit_video_button.render(to_render)

        window.blit(to_render, self.position)

        self.video_selector.render(window, self.position)
        self.audio_selector.render(window, self.position)

        self.anomaly_selector.render(window)

    def mouse_click_behavior(self, x, y):

        # Clickable check loop
        for clickable in self.soup:
            response = clickable.mouse_click_behavior(x, y, self.position)

            # Checking for responses from buttons
            match response:
                # Video submit button
                case "submit_video":
                    print(self.video_selector.selection)
                    self.display.respond_to_visual(self.display.active_goober.responses['Visual'][self.video_selector.selection], self.video_selector.selection)

                case "submit_audio":
                    if time.time() > self.audio_playable_timestamp:
                        audio_selection = self.audio_selector.selection
                        response = self.display.active_goober.responses['Sound'][audio_selection]
                        audio_duration = self.display.respond_to_audio(response, audio_selection)
                        self.audio_playable_timestamp = time.time() + audio_duration
                        self.submit_audio_button.change_text("Playing Audio")

                case "submit_type":
                    type_selection = self.anomaly_selector.selected_option
                    if type_selection == self.display.active_goober.type_name:
                        return "live"
                    else:
                        return "die"

            if response is not None:
                return response

class WebcamDisplay:
    def __init__(self,window):
        self.body = pygame.image.load(WEBCAM_PATH)
        self.body = pygame.transform.scale(self.body, WEBCAM_SIZE)
        self.active_goober = goober.random_goober(window)

        self.sprite = None
        self.last_visual_response = -1
        self.shake = -1

        self.last_goober_reaction = -1

        self.subtitles = components.SubtitleHolder(2, do_truncation=False)


    def respond_to_visual(self, respond, visual):

        if self.last_visual_response == -1:

            if respond:
                sprite = pygame.image.load(os.path.join("Assets","Visual","Response", visual) + ".png")
                self.shake = time.time() + 4 + random.random() * 2
            else:
                sprite = pygame.image.load(os.path.join("Assets","Visual",visual + ".png"))

            self.sprite = sprite
            self.sprite = pygame.transform.scale(self.sprite, WEBCAM_SIZE)
            self.last_visual_response = time.time()

    def respond_to_audio(self, respond, audio_name):

        if respond and random.randint(1, 5) > 1:
            audio = pygame.mixer.Sound(os.path.join("Assets", "Audio", "AudioCue_YesResponse", audio_name + ".mp3"))
            self.shake = time.time() + (audio.get_length() * (random.random() / 2 + 0.5))

        else:
            audio = pygame.mixer.Sound(os.path.join("Assets", "Audio", "AudioCue_NoResponse", audio_name + ".mp3"))

        audio.play()
        self.subtitles.add_subtitle("<" + audio_name[0] + audio_name[1:].lower() + ">", audio.get_length(), 0)

        return audio.get_length()

    def render(self, x, y, surface):

        if time.time() - self.last_visual_response > 4:
            self.last_visual_response = -1
            self.sprite = None
        
        if 1 > time.time() - self.shake > 0:
            if time.time() - self.last_goober_reaction > 1:
                self.last_goober_reaction = time.time()
                if random.randint(1, 5) > 1:
                    audio_name = random.choice(self.active_goober.reaction_sounds)
                    audio = pygame.mixer.Sound(os.path.join("Assets", "Audio", "ResponseAtmospheric", audio_name))
                    audio.play()
                    self.subtitles.add_subtitle("<" + audio_name[:-4] + ">", audio.get_length(), 1)
            goobx = math.sin(25 * (time.time() - self.shake)) / (time.time() - self.shake + 0.4)
        else:
            goobx = 0

        to_render = pygame.Surface(WEBCAM_SIZE)
        to_render.blit(self.body, (0, 0))
        to_render.blit(self.active_goober.sprite, (self.active_goober.position[0] + goobx, self.active_goober.position[1]))

        if self.sprite is not None:
            to_render.blit(self.sprite, (0, 0))
        self.subtitles.render(to_render, WEBCAM_SIZE[0] / 2 + 13, 300)

        surface.blit(to_render, (x, y))