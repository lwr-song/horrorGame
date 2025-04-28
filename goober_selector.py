import components

class GooberSelector:
    def __init__(self):
        self.HEIGHT = 250
        self.body = components.generate_window_sprite(1080, self.HEIGHT, "SELECTOR")

    def render(self, window):
        window.blit(self.body, (0, 720 - self.HEIGHT))


class ScrollingMenu:
    def __init__(self, options, position):
        self.options = options
        self.selected_option = 0
