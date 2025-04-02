import pygame
pygame.init()

MONITOR_INFO = pygame.display.Info()

MONITOR_HEIGHT = MONITOR_INFO.current_h
MONITOR_WIDTH = MONITOR_INFO.current_w

WIDTH = 480
HEIGHT = 360
window = pygame.display.set_mode([WIDTH, HEIGHT])

image = pygame.image.load("New Piskel.png")
window.blit(image, (0, 0))
pygame.display.flip()

input()
