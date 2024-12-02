import pygame.mixer
import random
from settings import Settings


class Game:
    """The game class"""

    def __init__(self, player, monster_group):
        """Set the attributes of the game  class"""
        # Initialize settings
        self.settings = Settings()

        # Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set sounds and music
        self.next_level_sound = pygame.mixer.Sound('assets/next_level.wav')

        # Set font
        self.font = pygame.font.Font('assets/Abrushow.ttf', 24)

        # Set images
        blue_image = pygame.image.load('assets/blue_monster.png')
        green_image = pygame.image.load('assets/green_monster.png')
        purple_image = pygame.image.load('assets/purple_monster.png')
        yellow_image = pygame.image.load('assets/yellow_monster.png')

        # This list corresponds to the monster_type attributes int
        # 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]
        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = self.settings.WIDTH // 2
        self.target_monster_rect.top = 30


    def update(self):
        """Update our game object"""
        self.round_time += 1

        # Check for collisions
        self.check_collisions()

    def draw(self):
        """Draw the HUD and other to the display"""
        # Set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # Add the monster colors to a list where the index of the color matches target_monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

    def check_collisions(self):
        """Check for collisions between player and monsters"""
        pass

    def start_new_round(self):
        """Populate bord with new monsters"""
        pass

    def choose_new_target(self):
        """Choose a new target monster for the player"""
        pass

    def pause_game(self):
        """Pause the game"""
        pass

    def reset_game(self):
        """Reset the game"""
        pass