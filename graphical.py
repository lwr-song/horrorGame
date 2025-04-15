# Graphical functions
import pygame, pygame.freetype, os
pygame.init()

TEXT_FONT = pygame.freetype.Font(os.path.join("Assets", "Fonts", "PixelDigivolve-mOm9.ttf"))

def generate_window(width, height, header_text, header_size=20):

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
    TEXT_FONT.fgcolor = (255, 255, 255)
    TEXT_FONT.size = header_size - 4
    TEXT_FONT.render_to(header, (2, 2), header_text)

    window_body = pygame.Rect(2, header_size, width - 4, height)

    pygame.draw.rect(new_window, (196, 196, 216), window_body)
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


class Dropdown:
    def __init__(self, options, width):

        if len(options) == 0:
            raise ValueError("Dropdowns one or more options")

        self.options = options
        self.selected_option = options[0]

        self.body = pygame.Surface((width, 20))
        innards = pygame.Surface((width - 4, 16))
        innards.fill((236, 236, 255))
        self.body.blit(innards, (2, 2))


