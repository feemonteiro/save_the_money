import pygame
import random
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(os.path.join(current_path,r'images\bill_100.png')).convert()
        self.surf = pygame.transform.rotozoom(self.surf, 0, 0.6)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                -random.randint(10, 100),
            )
        )

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()