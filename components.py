# Graphical functions
import pygame, pygame.freetype, os, time
pygame.init()

TF_HEADER = pygame.freetype.Font(os.path.join("Assets", "Fonts", "PixelDigivolve-mOm9.ttf"))

TF_BASIC = pygame.freetype.Font(os.path.join("Assets", "Fonts", "LcdSolid-VPzB.ttf"))
TF_BASIC.size = 16
TF_BASIC.fgcolor = (0, 0, 0)

TF_SUBTITLE = pygame.freetype.Font(os.path.join("Assets", "Fonts", "LcdSolid-VPzB.ttf"))
TF_SUBTITLE.size = 20
TF_SUBTITLE.fgcolor = (255, 255, 255)

AUTOFIT = -1

DROPDOWN_ARROW = pygame.image.load(os.path.join("Assets", "Sprites", "UI", "dropdown_down_arrow.png"))

def generate_window(width, height, header_text, header_size=20, color=(196, 196, 216)):

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

    window_body = pygame.Rect(2, header_size, width - 4, height - header_size - 2)

    pygame.draw.rect(new_window, color, window_body)
    new_window.blit(header, (2, 2))
    return new_window


def generate_button(width, height, shade_size=6):
    if width < 10:
        width = 10
    if height < 10:
        height = 10

    button = pygame.Surface((width, height))

    button_body = pygame.Surface((width - 2, height - 2))
    button_body.fill((196, 196, 216))
    shade = pygame.Surface((width - 2, shade_size))
    shade.fill((128, 128, 144))

    button_body.blit(shade, (0, height - (1 + shade_size)))
    button.blit(button_body, (1, 1))

    return button

class Button:
    def __init__(self, x, y, width, height, response, shade_size=6, group=None):

        if group is not None:
            group.append(self)

        self.body = generate_button(width, height, shade_size)
        self.width = width
        self.height = height
        self.response = response
        self.x, self.y, self.position = (x, y, (x, y))

    def render(self, window):
        window.blit(self.body, self.position)

    def mouse_click_behavior(self, x, y):
        if (self.x < x < self.x + self.width or
            self.y < y < self.y + self.height):
            return self.response


class Dropdown:
    def __init__(self, options, position, width=AUTOFIT, group=None):

        if len(options) == 0:
            raise ValueError("Dropdowns require one or more options")

        if width == AUTOFIT:
            sorted_options = sorted(options, key=len)
            width = TF_BASIC.get_rect(sorted_options[-1]).width + 30

        self.options = options
        self.selected_option = 0
        self.open = False
        self.position = position
        self.x, self.y = position
        self.WIDTH = width
        self.HEIGHT = 20

        self.body = pygame.Surface((width, self.HEIGHT))
        innards = pygame.Surface((width - 4, 16))
        innards.fill((236, 236, 255))
        self.body.blit(innards, (2, 2))
        self.body.blit(DROPDOWN_ARROW, (width - 18, 2))

        self.SELECTOR_HEIGHT = self.HEIGHT * len(self.options)
        self.selection_list = pygame.Surface((width, self.SELECTOR_HEIGHT))
        self.selection_list.fill((236, 236, 255))

        self.bottom_of_dropdown = self.y + self.HEIGHT
        self.overflow = (self.bottom_of_dropdown + self.SELECTOR_HEIGHT) > 720

        for i in range(len(self.options)):
            TF_BASIC.render_to(self.selection_list, (5, i * self.HEIGHT + 5), self.options[i])

        if group is not None:
            group.append(self)

    def render(self, window, relative_position=(0, 0)):

        x = self.x + relative_position[0]
        y = self.y + relative_position[1]
        
        window.blit(self.body, (x, y))
        TF_BASIC.render_to(window, (x + 5, y + 3), self.options[self.selected_option])

        if self.open:
            if self.overflow > 720:
                target_y = y - self.SELECTOR_HEIGHT
            else:
                target_y = self.bottom_of_dropdown
            window.blit(self.selection_list, (x, target_y))

    def mouse_click_behavior(self, mx, my, relative_position=(0, 0)):
        x = relative_position[0] + self.x
        y = relative_position[1] + self.y

        if x < mx < x + self.WIDTH:
            if self.open:
                if my > y + self.HEIGHT and self.overflow:
                    choice = (my - (y + self.HEIGHT)) // self.HEIGHT
                elif my < y and not self.overflow:
                    choice = len(self.options) - (y - my) // self.HEIGHT - 1
                else:
                    choice = self.selected_option

                if 0 <= choice < len(self.options):
                    self.selected_option = choice
                self.open = False
            elif y < my < y + self.HEIGHT:
                self.open = not self.open
        else:
            self.open = False

        return None


class Subtitle:
    def __init__(self, text, lifespan, priority=0):
        self.text = text
        self.lifespan = lifespan
        self.priority = priority
        self.time = 0

        self.start_measure = time.time()

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        return False

    def iterate(self):
        self.time += time.time() - self.start_measure
        self.start_measure = time.time()


class SubtitleHolder:
    def __init__(self, channels=1, do_truncation=True):
        self.channels = channels
        self.subtitle_list = []
        self.do_truncation = do_truncation

    def add_subtitle(self, text, lifespan, priority=0):
        self.subtitle_list.append(
            Subtitle(text, lifespan, priority)
        )

    @property
    def active_subtitles(self):
        self.subtitle_list.sort()
        if len(self.subtitle_list) <= self.channels:
            return self.subtitle_list[:]
        else:
            if self.do_truncation:
                self.subtitle_list = self.subtitle_list[-1:-(1 + self.channels):-1]
                return self.subtitle_list[:]
            else:
                return self.subtitle_list[-1:-(1 + self.channels):-1]

    def render(self, window, center_x, top_y):

        for subtitle in self.subtitle_list:
            subtitle.iterate()
            if subtitle.time > subtitle.lifespan:
                self.subtitle_list.remove(subtitle)

        subtitles = self.active_subtitles
        for i in range(len(subtitles)):
            focus_subtitle = subtitles[i]
            TF_SUBTITLE.render_to(
                window, (
                    center_x - TF_SUBTITLE.get_rect(focus_subtitle.text).width / 2,
                    top_y + 25 * i
                ), focus_subtitle.text
            )
            
