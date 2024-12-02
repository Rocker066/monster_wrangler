import pygame
from pygame.examples.aliens import Player

from settings import Settings
from player import Player
from game import Game
from monster import Monster


class MonsterWrangler:
    """The main class of monster wrangler game"""

    def __init__(self):
        """Set attributes of the class"""
        # Initialize pygame
        pygame.init()

        # instantiate the settings class
        self.settings = Settings()

        # Set the display surface and caption
        self.display_surface = pygame.display.set_mode((self.settings.WIDTH,
                                                        self.settings.HEIGHT))
        pygame.display.set_caption(self.settings.CAPTION)

        # Set the clock
        self.clock = pygame.time.Clock()

        # Set the state of the game
        self.running = True

        # Instantiate the player object and create its group
        self.my_player_group = pygame.sprite.Group()
        self.my_player = Player(self)
        self.my_player_group.add(self.my_player)

        # Create a monster group
        self.my_monster_group = pygame.sprite.Group()
        self.my_monster = Monster(500, 500, pygame.image.load('assets/blue_monster.png'), 0)
        self.my_monster_group.add(self.my_monster)
        self.my_monster2 = Monster(200, 500, pygame.image.load('assets/green_monster.png'), 1)
        self.my_monster_group.add(self.my_monster2)

        # Create a game object
        self.my_game = Game(self.my_player, self.my_monster_group)


    def run_game(self):
        """The main game loop"""
        while self.running:
            # Check to see if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the screen
            self.update_screen()


    def update_screen(self):
        """Update the display and blit assets"""
        # fill the screen
        self.display_surface.fill((0, 0, 0))

        # Update and draw sprite groups
        self.my_player_group.update()
        self.my_player_group.draw(self.display_surface)

        self.my_monster_group.update()
        self.my_monster_group.draw(self.display_surface)

        # Update and draw the game
        self.my_game.update()
        self.my_game.draw()

        # Flip the screen and tick the clock
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)


if __name__ == '__main__':
    mw = MonsterWrangler()
    mw.run_game()
