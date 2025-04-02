import pygame
pygame.init()

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 480
HEIGHT = 360
window = pygame.display.set_mode([WIDTH, HEIGHT])

#computer message functions


def send_message(user_window, sprite):

    pass

def click_button(button):

    pass

# Graphical functions
def generate_window(width, height, header_size=20):

    # Limiting parameters
    if header_size < 20:
        header_size = 20

    new_window = pygame.Surface((width, height + header_size))

    # Header generation
    header = pygame.Surface((width, header_size))
    gradations = max(20, int(width / 4))
    step_size = width / gradations

    # Creating the gradient in the header
    for i in range(gradations):
        x = i * step_size
        gradient_step = pygame.Surface((step_size + 1, header_size - 4))
        gradient_step.fill((0, 0, 200 - (100 * i / gradations)))
        header.blit(gradient_step, (x, 2))



    new_window.blit(header, (0, 0))
    return new_window

new_window = generate_window(300, 100)
window.blit(new_window, (0, 0))
pygame.display.flip()

input()

