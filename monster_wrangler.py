import pygame
import sys

from settings import Settings
from player import Player
from game import Game


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
        self.game_paused = False

        # hide the mouse
        pygame.mouse.set_visible(False)

        # Instantiate the player object and create its group
        self.my_player_group = pygame.sprite.Group()
        self.my_player = Player(self)
        self.my_player_group.add(self.my_player)

        # Create a monster group
        self.my_monster_group = pygame.sprite.Group()

        # Create a game object
        self.my_game = Game(self ,self.my_player, self.my_monster_group)
        self.my_game.pause_game('Monster Wrangler', 'Press ENTER to start')
        self.my_game.start_new_round()


    def run_game(self):
        """The main game loop"""
        while self.running:
            # Check to see if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.my_player.rect.y < self.settings.HEIGHT - 100:
                            self.my_player.warp()

                    # Pause  and unpause the game if escape is pressed
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused = not self.game_paused
                        self.my_game.paused()

            # If game is not paused then continue
            if not self.game_paused:
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
