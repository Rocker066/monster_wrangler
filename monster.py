from pygame.sprite import Sprite
import random
from settings import Settings


class Monster(Sprite):
    """A class to create enemy monster objects"""

    def __init__(self, x, y, image, monster_type):
        """Initialize the monster"""
        super().__init__()
        # Instantiate the setting
        self.settings = Settings()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Monster type is an int
        # 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.type = monster_type

        # Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 3)


    def update(self):
        """Update the monster"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # Bounce the monster off the edges of the display
        if self.rect.left <= 0 or self.rect.right >= self.settings.WIDTH:
            self.dx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= self.settings.HEIGHT - 100:
            self.dy *= -1