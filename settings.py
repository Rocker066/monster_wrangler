class Settings:
    """A class to store settings for monster wrangler game"""

    def __init__(self):
        """Define the attributes of settings class"""
        # Set the size of game window and caption
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.CAPTION = 'Monster Wrangler'

        # Set FPS
        self.FPS = 60

        # Set colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

