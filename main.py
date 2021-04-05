
from enum import Enum
import os
import time
from random import random

import pygame
import pygame.freetype
from pygame.sprite import RenderUpdates
from pygame.sprite import Sprite
from pygame.rect import Rect

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

from hero import Hero
from enemy import Enemy
from extra import Extra

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    ENDGAME = 3
    MENU = 4

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

    
class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

current_path = os.getcwd()

# Setup for sounds, defaults
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Save the Money - Alpha')
font = pygame.font.SysFont(None, 22)

# Create custom events for adding a new enemy, coins and new day
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)

NEWDAY = pygame.USEREVENT + 2
pygame.time.set_timer(NEWDAY, 10000) # each 10 seconds

ADDEXTRA = pygame.USEREVENT + 3
pygame.time.set_timer(ADDEXTRA, 9000) # each 9 seconds

# Variable to set game status
status = GameState.MENU

# Start Screen image
img_start = pygame.image.load(os.path.join(current_path,r'images\sky_init.png')) 

# Background music
pygame.mixer.music.load(os.path.join(current_path, 'sound/city.mp3'))
pygame.mixer.music.play(-1)

# background image
bg = pygame.image.load(os.path.join(current_path,r'images\sky.png'))

# create hero
hero = Hero()

enemies = pygame.sprite.Group()
extras = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)


# hero score
hero_score = 1200

# Initial day, enemy and enemy speed spawn
day = 1
enemy_speed = 5
new_enemy_speed = 2000

def start_screen(screen, status):

    # Start screen
    screen.fill((120, 120, 120))
    screen.blit(img_start, (0,0))

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RETURN):
                return GameState.NEWGAME
            if (event.key == pygame.K_ESCAPE):
                return GameState.QUIT
        if event.type == pygame.QUIT:
            return GameState.QUIT
    pygame.display.flip()
    
    return GameState.TITLE


def eng_game(screen, status, hero_score):

    bg_win = pygame.image.load(os.path.join(current_path,r'images\win.png'))
    bg_lose = pygame.image.load(os.path.join(current_path,r'images\lose.png'))

    # Creating background
    if hero_score > 0:
        screen.fill((120, 120, 120))
        screen.blit(bg_win, (0,0))
    else:
        screen.fill((120, 120, 120))
        screen.blit(bg_lose, (0,0))

    # stop music
    pygame.mixer.music.stop()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                return GameState.QUIT
        if event.type == pygame.QUIT:
            return GameState.QUIT

    pygame.display.flip()

    return GameState.ENDGAME

def title_screen(screen):
    start_btn = UIElement(
        center_position=(320, 280),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.TITLE,
    )
    quit_btn = UIElement(
        center_position=(320, 380),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    mouse_up = False
    for event in pygame.event.get():
        if event.type == QUIT:
            return GameState.QUIT
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up = True
    screen.fill(BLUE)

    for button in buttons:
        ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action

    buttons.draw(screen)
    pygame.display.flip()

    return GameState.MENU



# Game Loop
running = True

while running:
    
    # Initial screen
    if GameState.MENU == status:
        status = title_screen(screen)

    if GameState.TITLE == status:
        status = start_screen(screen, status)

    if GameState.NEWGAME == status:
        # Fill the screen with background image
        screen.blit(bg, (0,0))

        for event in pygame.event.get():
        # Did the user hit a key?
            if event.type == KEYDOWN:
                # Check if Escape key was pressed
                if event.key == K_ESCAPE:
                    running = False

            # Check if the user click the window close button
            elif event.type == QUIT:
                running = False

            # Should we add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy, and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDEXTRA:
                # Create the new coin, and add it to sprite groups
                new_extra = Extra()
                extras.add(new_extra)
                all_sprites.add(new_extra)
            
            elif event.type == NEWDAY:
                # increase day, enemy speed and the speed enemy is spawn
                day += 1
                enemy_speed += 1
                new_enemy_speed -= 200

                if new_enemy_speed <= 200:
                    new_enemy_speed = 200

                if enemy_speed > 23:
                    new_enemy_speed = 23

                if day == 15:
                    ADDEXTRA = pygame.USEREVENT + 3
                    pygame.time.set_timer(ADDEXTRA, 4000) # each 4 seconds


                ADDENEMY = pygame.USEREVENT + 1
                pygame.time.set_timer(ADDENEMY, new_enemy_speed)
                


        # Get the set of keys pressed and check for movement
        pressed_keys = pygame.key.get_pressed()
        hero.update(pressed_keys)

        # Update the position of enemies and extra coins
        enemies.update(enemy_speed)
        extras.update()

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # Display score
        text = font.render('Money: R$' + str(hero_score), True, (0, 0, 0))
        screen.blit(text, [510, 0])

        # Display Day
        text = font.render('Day: ' + str(day), True, (0, 0, 0))
        screen.blit(text, [10, 0])

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(hero, enemies):
            # Discount money
            hero_score -= 100
            # Remove bill
            pygame.sprite.spritecollide(hero, enemies, dokill=True)

            # # Stop any moving sounds and play the collision sound
            # collision_sound.play()
        
        # Check if any extra coins have collided with the player
        if pygame.sprite.spritecollideany(hero, extras):
            # Increase money
            hero_score += 50
            pygame.sprite.spritecollide(hero, extras, dokill=True)

        # If money is over or passed 30 days, game is over
        if hero_score < 0 or day == 30:
            hero.kill()
            status = GameState.ENDGAME

        # Flip everything to the display
        pygame.display.flip()

    if GameState.ENDGAME == status:
        status = eng_game(screen, status, hero_score)

    if GameState.QUIT == status:
        running = False

    # Ensure 30 frames per second rate
    clock.tick(30)
        


    

        

   
