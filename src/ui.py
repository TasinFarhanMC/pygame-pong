import pygame

class Text:
    def __init__(self, string: str, font: pygame.font.Font, pos, color = pygame.Color("white")):
        self.sur = font.render(string, True, color)
        self.size = self.sur.get_size()
        self.pos = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2

    def render(self, sur):
        sur.blit(self.sur, self.pos)

class Button():
    def __init__(self, text: Text):
        self.text = text
        self.rect: pygame.Rect

    def render(self, sur: pygame.Surface):
        self.text.render(sur)
        self.rect = pygame.Rect(self.text.pos[0], self.text.pos[1], self.text.size[0], self.text.size[1])

    def is_hovering(self, mouse_pos = None):
        if mouse_pos == None:
            return self.rect.collidepoint(pygame.mouse.get_pos())
        return self.rect.collidepoint(mouse_pos)
