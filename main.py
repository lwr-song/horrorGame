import pygame
import sys
pygame.init()

# This is so that if you get rid of New Piskel.png the game crashes
guy = pygame.image.load("New Piskel.png")

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 720
HEIGHT = 540
window = pygame.display.set_mode([WIDTH, HEIGHT], flags=pygame.FULLSCREEN)
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
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        pygame.display.flip()
        c.tick(30)


main_menu()