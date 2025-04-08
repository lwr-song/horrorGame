# Graphical functions
import pygame
pygame.init()

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
        gradient_step.fill((0, 0, 150 - (75 * i / gradations)))
        header.blit(gradient_step, (x, 0))

    window_body = pygame.Rect(2, header_size, width - 4, height)

    pygame.draw.rect(new_window, (196, 196, 196), window_body)
    new_window.blit(header, (2, 2))
    return new_window

def generate_button(width, height, shade_size=6):
    """
    Creates a Surface, which contains a button sprite.
    generate_button(int width, int height, int shade_size=6) => Surface

    int width
        The width of the button, which will automatically snap to be 10 if it is less than 10.

    int height
        The height of the button, which will automatically snap to be 10 if it is less than 10.

    int shade_size=6
        The size of the shading on the bottom part of the button
    """

    if width < 10:
        width = 10
    if height < 10:
        height = 10

    button = pygame.Surface((width, height))

    button_body = pygame.Surface((width - 2, height - 2))
    button_body.fill((196, 196, 196))
    shade = pygame.Surface((width - 2, shade_size))
    shade.fill((128, 128, 128))

    button_body.blit(shade, (0, height - (1 + shade_size)))
    button.blit(button_body, (1, 1))

    return button