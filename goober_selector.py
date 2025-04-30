import components
import pygame
import os
pygame.init()

OPTION = pygame.image.load(os.path.join("Assets", "Sprites", "UI", "selector_option.png"))
OPTION_HEIGHT = OPTION.get_rect().height
OPTION_WIDTH = OPTION.get_rect().width

class GooberSelector:
    def __init__(self, group=None):

        if group is not None:
            group.append(self)

        self.HEIGHT = 250
        self.body = components.generate_window_sprite(1080, self.HEIGHT, "SELECTOR")
        self.scrolling_menu = ScrollingMenu([
            "option " + str(i) for i in range(10)
        ], self.HEIGHT - 70)

    def render(self, window):
        to_render = pygame.Surface((1080, self.HEIGHT))
        to_render.blit(self.body, (0, 0))
        self.scrolling_menu.render(to_render, (1080 - OPTION_WIDTH - 24, 20))

        window.blit(to_render, (0, 720 - self.HEIGHT))

    def mouse_click_behavior(self, mx, my):
        response = self.scrolling_menu.mouse_click_behavior(mx, my, (1080 - OPTION_WIDTH - 24, 740 - self.HEIGHT))
        if response is not None:
            print(response)
        


class ScrollingMenu:
    def __init__(self, options, height):

        if len(options) == 0:
            raise ValueError("No can do boy")
        
        self.MAX_HEIGHT = len(options) * OPTION_HEIGHT - height

        self.options = options
        self.selected_option = 0
        self.height = height

        self.scroll = 0
        self.SCROLL_BAR_HEIGHT = self.height / (self.MAX_HEIGHT + self.height) * self.height

        self.conversion_factor = self.height - self.SCROLL_BAR_HEIGHT
        
        self.options_list = pygame.Surface((OPTION_WIDTH, len(self.options) * OPTION_HEIGHT))
        for i in range(len(self.options)):
            self.options_list.blit(OPTION, (0, OPTION_HEIGHT * i))
            components.TF_BASIC.render_to(self.options_list,
                (4, (i + 1/2) * OPTION_HEIGHT - components.TF_BASIC.get_rect(self.options[i]).height / 2),
                self.options[i])
    
    @property
    def scroll_bar(self):
        scroll_body = pygame.Surface((18, self.height))
        scroll_body.fill((96, 96, 108))

        scrolling_bar = pygame.Surface((18, self.SCROLL_BAR_HEIGHT))
        scrolling_bar.fill((196, 196, 216))
        
        scroll_body.blit(scrolling_bar, (0, self.scroll * (self.height - self.SCROLL_BAR_HEIGHT) / self.MAX_HEIGHT))

        return scroll_body
    
    def mouse_click_behavior(self, mx, my, relative_position=(0,0)):
        
        if relative_position[1] < my < self.height + relative_position[1]:
            if mx > OPTION_WIDTH + relative_position[0] + 4:
                self.scroll = max(0, min(self.MAX_HEIGHT,
                    (my - self.SCROLL_BAR_HEIGHT / 2 - relative_position[1]) / (self.height - self.SCROLL_BAR_HEIGHT) * self.MAX_HEIGHT
                                        ))
            elif relative_position[0] < mx:
                return self.options[int((my + self.scroll - relative_position[1]) / OPTION_HEIGHT)]
        return None

    def render(self, surface, position):
        to_render = pygame.Surface((OPTION_WIDTH + 22, self.height + 4))

        crop_rectangle = pygame.Rect(0, self.scroll, OPTION_WIDTH, self.height)
        to_render.blit(self.options_list, (0, 2), area=crop_rectangle)
        to_render.blit(self.scroll_bar, (OPTION_WIDTH + 2, 2))
        surface.blit(to_render, position)
