import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """A player class that the user can control"""

    def __init__(self, mw_game):
        """Initialize the player"""
        super().__init__()

        # Set settings
        self.settings = mw_game.settings

        # Set player image starting position and rect
        self.image = pygame.image.load('assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self.settings.WIDTH // 2
        self.rect.bottom = self.settings.HEIGHT

        # Set values
        self.lives = 5
        self.warps = 2
        self.velocity = 8

        # Set sound effects for the player
        self.catch_sound = pygame.mixer.Sound('assets/catch.wav')
        self.catch_sound.set_volume(.05)
        self.die_sound = pygame.mixer.Sound('assets/die.wav')
        self.die_sound.set_volume(.05)
        self.warp_sound = pygame.mixer.Sound('assets/warp.wav')
        self.warp_sound.set_volume(.05)


    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        # Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < self.settings.WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < self.settings.HEIGHT:
            self.rect.y += self.velocity


    def warp(self):
        """Warp the monster to the bottom (Safe Zone)"""
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = self.settings.HEIGHT


    def reset(self):
        """Resets the player position"""
        self.rect.centerx = self.settings.WIDTH // 2
        self.rect.bottom = self.settings.HEIGHT
