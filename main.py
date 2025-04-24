import pygame
import sys
import components, webcam
import goober



pygame.init()

# This is so that if you get rid of New Piskel.png the game crashes
guy = pygame.image.load("New Piskel.png")

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 1080
HEIGHT = 720
window = pygame.display.set_mode([WIDTH, HEIGHT])
c = pygame.time.Clock()

soup = []

guy = pygame.transform.scale(guy,(100,100))

# HELP ME! HEEELP!
def main_menu():
    window.blit(guy,(0,0))

    b = components.generate_window(WIDTH / 2, 300, "Woke")

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.blit(b, (0, 0))
        pygame.display.flip()
        c.tick(30)


def game_loop(day):

    roprown = webcam.Webcam((WIDTH / 2, 50), soup)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for clickable in soup:
                    clickable.mouse_click_behavior(x, y)

        window.fill((0, 0, 0))
        roprown.render(window)
        greachure = goober.Goober(window, "greg gregffley", "Shmingus")

        pygame.display.flip()



game_loop(1)
