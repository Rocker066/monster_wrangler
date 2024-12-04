import pygame.mixer
import random
import sys

from monster import Monster


class Game:
    """The game class"""

    def __init__(self, mw_game, player, monster_group):
        """Set the attributes of the game  class"""
        # Initialize settings
        self.settings = mw_game.settings
        self.screen = mw_game.display_surface
        self.running = mw_game.running

        # Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set sounds and music
        self.next_level_sound = pygame.mixer.Sound('assets/next_level.wav')
        self.next_level_sound.set_volume(.05)

        # Set font
        self.font = pygame.font.Font('assets/Abrushow.ttf', 24)
        self.font2 = pygame.font.Font('assets/Abrushow.ttf', 54)

        # Set images
        blue_image = pygame.image.load('assets/blue_monster.png')
        green_image = pygame.image.load('assets/green_monster.png')
        purple_image = pygame.image.load('assets/purple_monster.png')
        yellow_image = pygame.image.load('assets/yellow_monster.png')

        # Choose and show the target monster image
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
        self.frame_count += 1
        if self.frame_count == self.settings.FPS:
            self.round_time += 1
            self.frame_count = 0

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

        # Set text
        catch_text = self.font.render('Current Catch', True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = self.settings.WIDTH // 2
        catch_rect.top = 5

        score_text = self.font.render('Score: ' + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render('Lives: ' + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render('Current Round: ' + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render('Round Time: ' + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (self.settings.WIDTH - 10, 5)

        warp_text = self.font.render('Warps: ' + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (self.settings.WIDTH - 10, 35)

        # Blit the HUD and the current catch monster image
        self.screen.blit(catch_text, catch_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lives_text, lives_rect)
        self.screen.blit(round_text, round_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(warp_text, warp_rect)
        self.screen.blit(self.target_monster_image, self.target_monster_rect)
        # Draw a rect around monster catch image
        pygame.draw.rect(self.screen, colors[self.target_monster_type],
                         (self.settings.WIDTH // 2 - 32, 30, 64, 64), 2)
        # Draw a rect around our game area
        pygame.draw.rect(self.screen, colors[self.target_monster_type],
                         (0, 100, self.settings.WIDTH, self.settings.HEIGHT - 200), 4)


    def check_collisions(self):
        """Check for collisions between player and monsters"""
        # Check for collision between a player and an individual monster
        # We must test the type of monster to see if it matches the type of our target monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        # We collided with a monster
        if collided_monster:
            # Caught the CORRECT monster
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                # Remove the caught monster
                collided_monster.remove(self.monster_group)
                if self.monster_group:
                    # There are more correct monsters to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    # The round is complete
                    self.player.reset()
                    self.start_new_round()
            else:
                # Caught the WRONG monster
                self.player.die_sound.play()
                self.player.lives -= 1
                # Check for game over
                if self.player.lives <= 0:
                    self.pause_game('Final Score: ' + str(self.score), 'Press Enter to play again')
                    self.reset_game()
                self.player.reset()


    def start_new_round(self):
        """Populate bord with new monsters"""
        # Provide a score bonus based on how quickly the round was finished
        self.score += int(1000 * self.round_number / (1 + self.round_time))

        # Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        # Remove any remaining monsters from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add monsters to the monster group for the new round (populate the board)
        for i in range(self.round_number if self.round_number < 2 else self.round_number // 2):
            self.monster_group.add(Monster(random.randint(0, self.settings.WIDTH - 64),
                                           random.randint(100, self.settings.HEIGHT - 164),
                                           self.target_monster_images[0], 0))

            self.monster_group.add(Monster(random.randint(0, self.settings.WIDTH - 64),
                                           random.randint(100, self.settings.HEIGHT - 164),
                                           self.target_monster_images[1], 1))

            self.monster_group.add(Monster(random.randint(0, self.settings.WIDTH - 64),
                                           random.randint(100, self.settings.HEIGHT - 164),
                                           self.target_monster_images[2], 2))

            self.monster_group.add(Monster(random.randint(0, self.settings.WIDTH - 64),
                                           random.randint(100, self.settings.HEIGHT - 164),
                                           self.target_monster_images[3], 3))

        # Choose new target monster and play the next level sound effect
        self.choose_new_target()
        self.next_level_sound.play()


    def choose_new_target(self):
        """Choose a new target monster for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image


    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        # Create the main pause text
        main_text = self.font2.render(main_text, True, self.settings.RED)
        main_rect = main_text.get_rect()
        main_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2)

        # Create the sub pause text
        sub_text = self.font.render(sub_text, True, self.settings.WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 + 64)

        # Display the pause text
        self.screen.fill(self.settings.BLACK)
        self.screen.blit(main_text, main_rect)
        self.screen.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    # is_paused = False
                    sys.exit()


    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


    def paused(self):
        paused_text = self.font.render('PAUSED', True, self.settings.WHITE)
        paused_text_rect = paused_text.get_rect()
        paused_text_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2)

        self.screen.fill(self.settings.BLACK)
        self.screen.blit(paused_text, paused_text_rect)
        pygame.display.update()
