import components
import pygame
import os, json

pygame.init()

OPTION = pygame.image.load(os.path.join("Assets", "Sprites", "UI", "selector_option.png"))
OPTION_HEIGHT = OPTION.get_rect().height
OPTION_WIDTH = OPTION.get_rect().width

with open("AnomalyData.json") as file:
    anomaly_data = json.load(file)
with open("DescriptionData.json") as file:
    description_data = json.load(file)

class GooberSelector:
    def __init__(self, group=None):

        # This class is clickable, so it must be part of a group
        if group is not None:
            group.append(self)

        self.HEIGHT = 250
        self.body = components.generate_window_sprite(1080, self.HEIGHT, "SELECTOR")
        self.scrolling_menu = ScrollingMenu(list(anomaly_data.keys()), self.HEIGHT - 70)
        self.goober_display = GooberDisplay(1080 - OPTION_WIDTH - 30, self.HEIGHT - 70)

        # Building currently selected crucible
        selection_display_rect = pygame.Rect(1080 - OPTION_WIDTH - 24, self.HEIGHT - 40, OPTION_WIDTH, 30)
        pygame.draw.rect(self.body, (236, 236, 255), selection_display_rect)

        # Button for submitting type
        self.submit_type_button = components.Button(
            400,
            self.HEIGHT - 40,
            250,
            35,
            "submit_type",
            "Submit Type",
            text_size=16
        )

        # The currently selected option in this window's ScrollingMenu
        self.selected_option = None

    def render(self, window):
        position = (0, 720 - self.HEIGHT)
        to_render = pygame.Surface((1080, self.HEIGHT))
        to_render.blit(self.body, (0, 0))

        if self.selected_option is not None:
            components.TF_BASIC.render_to(to_render, (1080 - OPTION_WIDTH - 19, self.HEIGHT - 30), self.selected_option)

        self.scrolling_menu.render(to_render, (1080 - OPTION_WIDTH - 24, 20))
        self.goober_display.render(4, 22, to_render, self.selected_option)

        self.submit_type_button.render(to_render)

        window.blit(to_render, position)

    def mouse_click_behavior(self, mx, my, blah):
        # blah is there because it would break otherwise

        # Submit type of goober button check
        if self.submit_type_button.mouse_click_behavior(mx, my, (0, 720 - self.HEIGHT)):
            return "submit_type"

        # Selecting something from the scrolling menu
        response = self.scrolling_menu.mouse_click_behavior(mx, my, (1080 - OPTION_WIDTH - 24, 740 - self.HEIGHT))
        if response is not None:
            self.selected_option = response




class ScrollingMenu:
    def __init__(self, options, height):

        if len(options) == 0:
            raise ValueError("No can do boy")
        
        self.MAX_HEIGHT = len(options) * OPTION_HEIGHT - height

        self.options = options
        self.options.sort()
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
        # This function gets a surface with the height and width of the appropriate scroll bar
        scroll_body = pygame.Surface((18, self.height))
        scroll_body.fill((96, 96, 108))

        scrolling_bar = pygame.Surface((18, self.SCROLL_BAR_HEIGHT))
        scrolling_bar.fill((196, 196, 216))
        
        scroll_body.blit(scrolling_bar, (0, self.scroll * (self.height - self.SCROLL_BAR_HEIGHT) / self.MAX_HEIGHT))

        return scroll_body
    
    def mouse_click_behavior(self, mx, my, relative_position=(0,0)):

        # Collision check
        if relative_position[1] < my < self.height + relative_position[1]:

            # For scrolling the scroll bar
            if mx > OPTION_WIDTH + relative_position[0]:
                self.scroll = max(0, min(self.MAX_HEIGHT,
                    (my - self.SCROLL_BAR_HEIGHT / 2 - relative_position[1]) / (self.height - self.SCROLL_BAR_HEIGHT) * self.MAX_HEIGHT
                                        ))

            # Selecting an option from the list
            elif relative_position[0] < mx:
                return self.options[int((my + self.scroll - relative_position[1]) / OPTION_HEIGHT)]
        return None

    def render(self, surface, position):
        to_render = pygame.Surface((OPTION_WIDTH + 22, self.height + 4))

        crop_rectangle = pygame.Rect(0, self.scroll, OPTION_WIDTH, self.height)
        to_render.blit(self.options_list, (0, 2), area=crop_rectangle)
        to_render.blit(self.scroll_bar, (OPTION_WIDTH + 2, 2))
        surface.blit(to_render, position)

class GooberDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.body = pygame.Surface((width, height))

        interior = pygame.Surface((width - 4, height - 4))
        interior.fill((216, 216, 236))
        self.body.blit(interior, (2, 2))

        self.display = pygame.Surface((height - 8, height - 12))

    def render(self, x, y, surface, goober):
        surface.blit(self.body, (x, y))
        if goober is None:
            text = ["No anomaly selected."]
        else:
            goober_data = anomaly_data[goober]

            identity_description = description_data["Sprite"][goober_data["Sprite"]]
            behavior_description = description_data["Behavior"][goober_data["Behavior"]]

            text = identity_description + [""] + behavior_description

            self.display.fill((196, 196, 216))
            sprite = pygame.image.load(os.path.join("Assets", "Sprites", "Goober", anomaly_data[goober]["Sprite"]))

            spright = sprite.get_rect().height #it stands for sprite height
            spridth = sprite.get_rect().width # Same
            if spright < self.height - 12:
                sprite = pygame.transform.scale(sprite, (spridth * ((self.height - 8) / spright), self.height - 12))

            self.display.blit(sprite, ((self.height - 8) / 2 - spridth / 2, 0))
            surface.blit(self.display, (x + self.width - (self.height - 8) - 4, y + 6))

        for i in range(len(text)):
            line = text[i]
            components.TF_BASIC.render_to(surface, (x + 4, y + 4 + 20 * i), line)