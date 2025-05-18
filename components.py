# Graphical functions
import pygame, pygame.freetype, os, time

pygame.init()

# Default font sizes
TF_HEADER_DEFAULT_SIZE = 20
TF_BASIC_DEFAULT_SIZE = 16
TF_SUBTITLE_DEFAULT_SIZE = 20

# Text font used for window headers
TF_HEADER = pygame.freetype.Font(os.path.join("Assets", "Fonts", "PixelDigivolve-mOm9.ttf"))

# Text font used for basic window text (such as the text on the stimulus selection window)
TF_BASIC = pygame.freetype.Font(os.path.join("Assets", "Fonts", "CiGamedevRegular-ovq3z.ttf"))
TF_BASIC.size = TF_BASIC_DEFAULT_SIZE
TF_BASIC.fgcolor = (0, 0, 0)

# Text font used for subtitles, which is drawn on the webcam window
TF_SUBTITLE = pygame.freetype.Font(os.path.join("Assets", "Fonts", "CiGamedevRegular-ovq3z.ttf"))
TF_SUBTITLE.size = TF_SUBTITLE_DEFAULT_SIZE
TF_SUBTITLE.fgcolor = (255, 255, 255)

DROPDOWN_ARROW = pygame.image.load(os.path.join("Assets", "Sprites", "UI", "dropdown_down_arrow.png"))

# Generates the sprite for windows
def generate_window_sprite(width, height, header_text, header_size=20, color=(196, 196, 216)):

    # Limiting parameters
    if header_size < 20:
        header_size = 20

    new_window = pygame.Surface((width, height + header_size))
    new_window.fill((32, 32, 32))

    # Header generation
    header = pygame.Surface((width - 4, header_size - 4))
    gradations = max(20, int((width - 4) / 4))
    step_size = (width - 4) / gradations

    # Creating the gradient in the header
    for i in range(gradations):
        x = i * step_size
        gradient_step = pygame.Surface((step_size + 1, header_size))
        gradient_step.fill((0, 0, 216 - (96 * i / gradations)))
        header.blit(gradient_step, (x, 0))

    # Header text
    TF_HEADER.fgcolor = (255, 255, 255)
    TF_HEADER.size = header_size - 4
    TF_HEADER.render_to(header, (2, 2), header_text)

    # The main body of the window
    window_body = pygame.Rect(2, header_size, width - 4, height - 2)

    # Compositing the window and the header into the real window
    pygame.draw.rect(new_window, color, window_body)
    new_window.blit(header, (2, 2))
    return new_window


# Generates the sprite used for the button
def generate_button_sprite(width, height, text, text_size, shade_size=6):

    # Limiting parameters
    if width < 10:
        width = 10
    if height < 10:
        height = 10

    button = pygame.Surface((width, height))

    # Compositing the button image together
    button_body = pygame.Surface((width - 2, height - 2))
    button_body.fill((196, 196, 216))
    shade = pygame.Surface((width - 2, shade_size))
    shade.fill((128, 128, 144))
    highlight = pygame.Surface((width - 2, shade_size))
    highlight.fill((236, 236, 255))

    button_body.blit(shade, (0, height - (1 + shade_size)))
    button_body.blit(highlight, (0, 1))
    button.blit(button_body, (1, 1))

    TF_BASIC.size = text_size

    # Drawing text on the button
    text_rect = TF_BASIC.get_rect(text)

    # Aligning the text to the center of the button
    TF_BASIC.render_to(button, (width / 2 - text_rect.width / 2,
                              (height - shade_size) / 2 - text_rect.height / 2),
                       text)

    TF_BASIC.size = TF_BASIC_DEFAULT_SIZE
    
    return button


# Button class
class Button:
    def __init__(self, x, y, width, height, response, text, shade_size=3, group=None, text_size=TF_BASIC_DEFAULT_SIZE):

        # This class is clickable, so it should be in a group (Soup)
        if group is not None:
            group.append(self)

        self.visible = True
        self.body = generate_button_sprite(width, height, text, text_size, shade_size)
        self.width = width
        self.height = height
        self.text_size = text_size
        self.shade_size = shade_size
        self.text = text
        self.response = response # This response will be returned when this button is pressed
        self.x, self.y = (x, y)
        
    def render(self, window):
        window.blit(self.body, (self.x, self.y))

    def mouse_click_behavior(self, mx, my, relative_position=(0,0)):
        x = self.x + relative_position[0]
        y = self.y + relative_position[1]
        if (x < mx < x + self.width and
            y < my < y + self.height):
                # Check for this response later in order to perform
                # certain functions
                return self.response
    
    def change_text(self, text):
        self.body = generate_button_sprite(self.width, self.height, text, self.text_size, self.shade_size)
        self.text = text

# Dropdown class
class Dropdown:
    def __init__(self, options, position, width, group=None):

        # Dropdowns with 0 options would literally be useless btw
        if len(options) == 0:
            raise ValueError("Dropdowns require one or more options")

        self.options = options # The list of options to select from 
        self.selected_option = 0 # The index of the currently selected option
        self.open = False # Whether the dropdown is open
        self.x, self.y = position
        self.WIDTH = width
        self.HEIGHT = 20

        # Constructing the dropdown menu's main body
        self.body = pygame.Surface((width, self.HEIGHT))
        innards = pygame.Surface((width - 4, 16))
        innards.fill((236, 236, 255))
        self.body.blit(innards, (2, 2))
        self.body.blit(DROPDOWN_ARROW, (width - 18, 2))

        # Constructing the sprite to show the list of options to select from
        self.SELECTOR_HEIGHT = self.HEIGHT * len(self.options)
        self.selection_list = pygame.Surface((width, self.SELECTOR_HEIGHT))
        self.selection_list.fill((236, 236, 255))

        # Printing text onto the list of options sprite
        for i in range(len(self.options)):
            TF_BASIC.render_to(self.selection_list, (5, i * self.HEIGHT + 5), self.options[i])

        # Dropdowns are clickable, so they should be in a group (Soup)
        if group is not None:
            group.append(self)

    # Returns whether the dropdown menu would overflow off of the screen if it was opened
    def is_overflow(self, relative_position=(0, 0)):
        bottom_of_dropdown = self.y + self.HEIGHT + relative_position[1]

        # This relies on the window height being constant
        # Change this as well if you want to change the window size
        # Doesn't get affected by fullscreen
        return bottom_of_dropdown + self.SELECTOR_HEIGHT > 720

    # Rendering function
    def render(self, window, relative_position=(0, 0)):

        x = self.x + relative_position[0]
        y = self.y + relative_position[1]
        
        window.blit(self.body, (x, y))
        # Drawing the currently selected option
        TF_BASIC.render_to(window, (x + 5, y + 3), self.options[self.selected_option])

        if self.open:
            bottom_of_dropdown = y + self.HEIGHT
            # Deciding whether to open the dropdown upwards or downwards
            # based on whether it will overflow off the screen when opened
            if bottom_of_dropdown + self.SELECTOR_HEIGHT > 720:
                target_y = y - self.SELECTOR_HEIGHT
            else:
                target_y = bottom_of_dropdown
            window.blit(self.selection_list, (x, target_y))
    
    # Mouse click behavior
    def mouse_click_behavior(self, mx, my, relative_position=(0, 0)):

        x = relative_position[0] + self.x
        y = relative_position[1] + self.y

        # Click detection
        if x < mx < x + self.WIDTH:
            if self.open:
                is_overflow = self.is_overflow(relative_position)

                # Option selection
                # I could explain this better but it works
                # So it's not really necessary
                # Don't change it :)
                if my > y + self.HEIGHT and not is_overflow:
                    choice = (my - (y + self.HEIGHT)) // self.HEIGHT
                elif my < y and is_overflow:
                    choice = len(self.options) - (y - my) // self.HEIGHT - 1
                else:
                    choice = self.selected_option

                if 0 <= choice < len(self.options):
                    self.selected_option = choice
                self.open = False
                return True
            elif y < my < y + self.HEIGHT:
                self.open = not self.open
                return True
        else:
            self.open = False

        return None

    # Property that returns the currently selected element of the dropdown's options
    @property
    def selection(self):
        return self.options[self.selected_option]

# Subtitle class
"""
The Subtitle class contains a priority attribute, which affects how the 
SubtitleHolder class renders the subtitles
The SubtitleHolder class only has a select number of channels, which is the
number of subtitles it will render at any time. So, for example, if it had 3
channels, it could only render 3 subtitles at a time
The priority attribute affects which subtitles are rendered. Higher priority
subtitles are rendered over lower priority subtitles
"""
class Subtitle:
    def __init__(self, text, lifespan, priority=0, offset=0):
        self.text = text
        self.lifespan = lifespan
        self.priority = priority
        self.time = -offset

        self.start_measure = time.time()

    def __lt__(self, other):
        # For sorting subtitles by subtitle priority
        if self.priority < other.priority:
            return True
        return False

    def iterate(self):
        # Incrementing the time
        # This is so the subtitle can be killed once it exceeds its lifespan
        self.time += time.time() - self.start_measure
        self.start_measure = time.time()

    def render(self, window, position):
        # fgcolor setting is for the fadeout
        TF_SUBTITLE.fgcolor=[max(0, min(255, int(255 * (1 - self.time + self.lifespan - 1)))) for i in range(3)]
        TF_SUBTITLE.render_to(window, position, self.text)


# SubtitleHolder composite class
class SubtitleHolder:
    def __init__(self, channels=1, do_truncation=True):
        self.channels = channels # The maximum number of subtitles that can be rendered at once
        self.subtitle_list = []

        # This attribute makes it so that if a high priority subtitle is rendered,
        # all existing low priority subtitles are instantly removed from the list
        self.do_truncation = do_truncation

    # Adding a subtitle to the SubtitleHolder
    def add_subtitle(self, text, lifespan, priority=0):
        self.subtitle_list.append(
            Subtitle(text, lifespan, priority)
        )

    # Gets which subtitles to render
    @property
    def active_subtitles(self):
        # Priority sorting
        self.subtitle_list.sort()

        # If there are fewer subtitles than channels, the number of subtitles
        # doesn't matter
        if len(self.subtitle_list) <= self.channels:
            return self.subtitle_list[:]
        else:
            if self.do_truncation:
                # Truncating list
                self.subtitle_list = self.subtitle_list[-1:-(1 + self.channels):-1]
                return self.subtitle_list[:]
            else:
                return self.subtitle_list[-1:-(1 + self.channels):-1]

    def render(self, window, center_x, top_y):

        for subtitle in self.subtitle_list:
            # Changing subtitle times and removing them if they exceed
            # their lifespan
            subtitle.iterate()
            if subtitle.time > subtitle.lifespan:
                self.subtitle_list.remove(subtitle)

        subtitles = self.active_subtitles
        subtitles.reverse()
        for i in range(len(subtitles)):
            focus_subtitle = subtitles[i]

            # Certain subtitles can be set to only appear after time has passed
            # (offset attribute in subtitle class)
            # This check ensures that they will not render early
            if focus_subtitle.time > 0:
                focus_subtitle.render(
                    window, (
                        center_x - TF_SUBTITLE.get_rect(focus_subtitle.text).width / 2,
                        top_y + 20 * i
                    )
                )
            
