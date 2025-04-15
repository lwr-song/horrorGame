import pygame
import sys
import graphical, webcam
pygame.init()

# This is so that if you get rid of New Piskel.png the game crashes
guy = pygame.image.load("New Piskel.png")

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 720
HEIGHT = 540
window = pygame.display.set_mode([WIDTH, HEIGHT])
c = pygame.time.Clock()

#computer message functions

guy = pygame.transform.scale(guy,(100,100))
def send_message(user_window, sprite):

    pass

def click_button(button):

    pass



# HELP ME! HEEELP!
def main_menu():
    window.blit(guy,(0,0))

    b = graphical.generate_window(300, 300, "Woke")

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.blit(b, (0, 0))
        pygame.display.flip()
        c.tick(30)


def game_loop(day):

    roprown = graphical.Dropdown(["my father", "my brother", "my mother"], 200)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        roprown.render(window, 0, 0)

        pygame.display.flip()



game_loop(1)