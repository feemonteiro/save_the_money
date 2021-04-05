import pygame
import os

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

current_path = os.getcwd()
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super(Hero, self).__init__()
        self.surf = pygame.image.load(os.path.join(current_path,r'images\hero.png')).convert()
        self.surf = pygame.transform.rotozoom(self.surf, 0, 0.5)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                320,
                420,
            )
        )

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
