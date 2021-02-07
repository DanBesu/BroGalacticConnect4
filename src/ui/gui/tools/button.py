import pygame

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Button:
    def __init__(self, screen, px, py, width, height, color1, color2, text):
        self.__screen = screen
        self.px = px
        self.py = py
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        self.text = text

    def is_in_button_range(self, mouse):
        if self.px <= mouse[0] <= self.px + self.width and self.py <= mouse[1] <= self.py + self.height:
            return True
        return False

    def draw(self, mouse):

        if self.is_in_button_range(mouse):
            pygame.draw.rect(self.__screen, YELLOW, (self.px, self.py, self.width, self.height))
        else:
            pygame.draw.rect(self.__screen, WHITE, (self.px, self.py, self.width, self.height))
        self.__screen.blit(self.text, (self.px, self.py))
