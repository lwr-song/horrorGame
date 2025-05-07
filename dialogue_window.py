import pygame
import components
pygame.init()

class DialogueWindow:
    def __init__(self, center, dialogue_list):
        self.body = components.generate_window_sprite(540, 180, "INCOMING CALL")
        self.center = center

        self.rendered_dialogue = []
        self.dialogue_list = dialogue_list
        self.dialogue_index = 0
        self.letter_index = 0

        self.loaded_dialogue = self.dialogue_list[self.dialogue_index]
        self.current_dialogue_length = 0

    def load_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue_list):
            return False

    def render(self, position, window):
        components.TF_BASIC.size = 24
        to_render = pygame.Surface((540, 180))
        to_render.blit(self.body, (0, 0))

        for i in range(len(self.rendered_dialogue)):
            components.TF_BASIC.render_to(to_render, (105, 30 + 30 * i), self.rendered_dialogue[i])

        window.blit(to_render, (self.center[0] - 270, self.center[1] - 180))
        components.TF_BASIC.size = components.TF_BASIC_DEFAULT_SIZE

    def update(self):

        if self.letter_index >= len(self.dialogue_list[self.dialogue_index]):
            return

        components.TF_BASIC.size = 24
        if len(self.rendered_dialogue) == 0:
            self.current_dialogue_length = 0
            self.rendered_dialogue.append("")

        if (self.current_dialogue_length
            + components.TF_BASIC.get_rect(self.dialogue_list[self.dialogue_index][self.letter_index]).width) > 420:
            self.current_dialogue_length = 0

            split_words = self.rendered_dialogue[-1].split(" ")
            self.rendered_dialogue[-1] = " ".join(split_words[-1::-1])
            self.rendered_dialogue.append(split_words[-1])

        self.rendered_dialogue[-1] += self.dialogue_list[self.dialogue_index][self.letter_index]
        self.letter_index += 1
        self.current_dialogue_length = components.TF_BASIC.get_rect(self.rendered_dialogue[-1]).width

        components.TF_BASIC.size = components.TF_BASIC_DEFAULT_SIZE