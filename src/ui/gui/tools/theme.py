import pygame


class Theme:
    def __init__(self, name='galactic',
                 background_image=pygame.image.load('images/galaxy_background.jpeg'),
                 player_image=pygame.image.load('images/tesla_cut.png'),
                 computer_image=pygame.image.load('images/ufo_cut.png'),
                 font=pygame.font.SysFont("images/monospace", 75),
                 transition_image=pygame.image.load('images/galaxy_transition.jpeg')):
        self.name = name
        self.background = background_image
        self.player_image = player_image
        self.computer_image = computer_image
        self.font = font
        self.transition_image = transition_image
