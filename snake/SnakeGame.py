# Import necessary libraries
import pygame
from pygame.locals import *
import sys
from pygame.math import Vector2
import time
import random

# Initialize pygame
pygame.init()

# Game mode: 0 = Walls, 1 = No Walls (wrap around)
game_mode = 0  # Default to Walls mode

# Screen setup
width = 800  # Default width (changed to 800)
height = 600  # Default height (changed to 600)
tile_size = 35
screen = pygame.display.set_mode((width, height))  # Windowed mode by default

# Dark/Light Mode
dark_mode = False
background_day = pygame.image.load("images/day_background.png")  # Light mode background
background_night = pygame.image.load("images/night_background.png")  # Dark mode background
background = background_day  # Default to light mode

# Load images, rects, and masks
snake = pygame.image.load("images/snakeIcon.png")
startImg = pygame.image.load("images/start_btn.png")
exitImg = pygame.image.load("images/exit_btn.png")
optionsImg = pygame.image.load("images/options_btn.png")  # Options button image
pauseImg = pygame.image.load("images/pause.png")
snakeHeadRight = pygame.image.load("images/snakeHeadRight.png")
snakeHeadLeft = pygame.image.load("images/snakeHeadLeft.png")
snakeHeadUp = pygame.image.load("images/snakeHeadUp.png")
snakeHeadDown = pygame.image.load("images/snakeHeadDown.png")
snakeHead = snakeHeadDown  # Initial head image
snakeheadMask = pygame.mask.from_surface(snakeHead)
headRect = snakeHead.get_rect()
headRect.topleft = (38, 38)
snakebody = pygame.image.load("images/body.jpg")
heart1 = pygame.image.load("images/heart.png")
heart2 = pygame.image.load("images/heart.png")
heart3 = pygame.image.load("images/heart.png")
heartRect = heart1.get_rect()
heartRect.topright = (width - 10, 5)
heartRect2 = heart2.get_rect()
heartRect2.topright = (width - 60, 5)
heartRect3 = heart3.get_rect()
heartRect3.topright = (width - 110, 5)
soldier = pygame.image.load("images/soldier.png")
deadApple = pygame.image.load("images/poison_apple.png")
deadAppleRect = deadApple.get_rect()
deadAppleRect.topleft = (200, 300)
deadAppleMask = pygame.mask.from_surface(deadApple)
bulletImg = pygame.image.load("images/bullet.png")
bulletRect = bulletImg.get_rect()
bulletRect.center = soldier.get_rect().center
bulletMask = pygame.mask.from_surface(bulletImg)

# Load sounds
mainMusic = pygame.mixer.Sound("sounds/sounds_main.mp3")
mainMusic.set_volume(0.2)
mainMusic.play(-1)  # Loop main music
gameOverMusic = pygame.mixer.Sound("sounds/sounds_gameOver.mp3")
gameOverMusic.set_volume(1)
winMusic = pygame.mixer.Sound("sounds/sounds_win.mp3")
winMusic.set_volume(1)
click = pygame.mixer.Sound("sounds/sounds_click.wav")
click.set_volume(1)
lostLife = pygame.mixer.Sound("sounds/sounds_lostLife.mp3")
lostLife.set_volume(1)
good = pygame.mixer.Sound("sounds/sounds_goodResult.mp3")
good.set_volume(1)

# Define colors
fontColor = (240, 240, 240)
Black = (0, 0, 0)
White = (255, 255, 255)
Highlight = (255, 200, 0)

# Set window caption and icon
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(snake)

# Initialize important variables
clock = pygame.time.Clock()
pause = False
hitCount = 0
appleCount = 0
daimondCount = 0
bullet_speed = 20
bullet_active = False
fontscore = pygame.font.SysFont('Elephant', 15)
snake_segments = [(38, 38)]

# Resolution options
resolutions = [
    (800, 600),  # Default resolution (changed to 800x600)
    (1024, 768),
    (1280, 720),
    (1920, 1080)
]

# Game modes
game_modes = ["Windowed", "Borderless", "Fullscreen"]

# Level data for Border Mode
level1_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

level2_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 9, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 5, 0, 0, 8, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 8, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# New Level 3 Data
level3_data=[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 9, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 5, 0, 0, 8, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 8, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Class for buttons
class Button():
    def __init__(self, x, y, image, scale):
        # Initialize button properties
        Bwidth = image.get_width()
        Bheight = image.get_height()
        self.image = pygame.transform.scale(image, (int(Bwidth * scale), int(Bheight * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        # Draw the button and handle click events
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):  # Check if mouse is over the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # Left mouse button clicked
                self.clicked = True
                click.play()  # Play click sound
                action = True

            if pygame.mouse.get_pressed()[0] == 0:  # Button released
                self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))  # Draw the button
        return action  # Return whether the button was clicked

# Function to render text
def TextThings(text, font, color=fontColor):
    # Render text and return the surface and rect
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Function to display score text
def ScoreText(text, font, text_col, x, y):
    # Render and display score text
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Apple class for collectible items
class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/apple.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Create groups for apples and diamonds
appleGroup = pygame.sprite.Group()
appleGroup2 = pygame.sprite.Group()
appleGroup3 = pygame.sprite.Group()

# Diamond class for collectible items
class Daimond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/diamond.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Create groups for diamonds
daimondGroup = pygame.sprite.Group()
daimondGroup2 = pygame.sprite.Group()
daimondGroup3 = pygame.sprite.Group()

# HeadSprite class for the snake's head
class HeadSprite(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill((255, 0, 0))  # Red color for debugging
        self.rect = rect

# Create an instance of the HeadSprite
head_sprite = HeadSprite(headRect)

# World class to handle level design and collisions
class world():
    def __init__(self, data):
        # Load images for tiles
        miniT1_img = pygame.image.load('images/miniTree1.png')
        miniT2_img = pygame.image.load('images/miniTree2.png')
        miniT3_img = pygame.image.load('images/miniTree3.png')
        rocks = pygame.image.load('images/rocks.jpg')
        mushroom = pygame.image.load('images/mushroom.webp')

        self.tile_list = []  # List to hold tiles
        self.mask_list = []  # List to hold masks for collision detection
        row_count = 0

        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Rock tile
                    img = pygame.transform.scale(rocks, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.mask_list.append(pygame.mask.from_surface(img))
                if tile == 2:  # Mini Tree 1
                    img = pygame.transform.scale(miniT1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.mask_list.append(pygame.mask.from_surface(img))
                if tile == 3:  # Mini Tree 2
                    img = pygame.transform.scale(miniT2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.mask_list.append(pygame.mask.from_surface(img))
                if tile == 4:  # Mini Tree 3
                    img = pygame.transform.scale(miniT3_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.mask_list.append(pygame.mask.from_surface(img))
                if tile == 5:  # Mushroom
                    img = pygame.transform.scale(mushroom, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    self.mask_list.append(pygame.mask.from_surface(img))
                if tile == 6:  # Apple
                    apple = Apple(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    appleGroup.add(apple)
                if tile == 7:  # Diamond
                    daimond = Daimond(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    daimondGroup.add(daimond)
                if tile == 8:  # Apple for Level 2
                    apple2 = Apple(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    appleGroup2.add(apple2)
                if tile == 9:  # Diamond for Level 2
                    daimond2 = Daimond(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    daimondGroup2.add(daimond2)
                if tile == 10:  # Apple for Level 3
                    apple3 = Apple(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    appleGroup3.add(apple3)
                if tile == 11:  # Diamond for Level 3
                    daimond3 = Daimond(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    daimondGroup3.add(daimond3)
                col_count += 1
            row_count += 1

    def draw(self):
        # Draw all tiles in the level
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def check_collision(self, headRect, snakeheadMask):
        # Check for collisions between the snake's head and tiles
        for tile, mask in zip(self.tile_list, self.mask_list):
            if mask:  # Only check tiles with masks
                offset = (headRect.x - tile[1].x, headRect.y - tile[1].y)
                if mask.overlap(snakeheadMask, offset):  # Check for overlap
                    return True
        return False

# Generate level data for No Border Mode (no walls)
def generate_no_border_level_data(width, height, tile_size):
    # Create an empty level data grid
    level_data = []
    for row in range(height // tile_size):
        level_row = []
        for col in range(width // tile_size):
            level_row.append(0)  # Empty space
        level_data.append(level_row)

    # Add apples and diamonds to the level data
    for _ in range(5):  # Add 5 apples
        row = random.randint(1, (height // tile_size) - 2)
        col = random.randint(1, (width // tile_size) - 2)
        level_data[row][col] = 6  # 6 represents an apple

    for _ in range(3):  # Add 3 diamonds
        row = random.randint(1, (height // tile_size) - 2)
        col = random.randint(1, (width // tile_size) - 2)
        level_data[row][col] = 7  # 7 represents a diamond

    return level_data

# Initialize level data based on game mode
if game_mode == 0:  # Border Mode
    level1 = world(level1_data)
    level2 = world(level2_data)
    level3 = world(level3_data)  # Initialize level 3
else:  # No Border Mode
    level1_data = generate_no_border_level_data(width, height, tile_size)
    level2_data = generate_no_border_level_data(width, height, tile_size)
    level3_data = generate_no_border_level_data(width, height, tile_size)  # Generate level 3 data
    level1 = world(level1_data)
    level2 = world(level2_data)
    level3 = world(level3_data)  # Initialize level 3

# Center the buttons
start = Button(width // 2 - 100, height // 2 - 100, startImg, 0.8)
options = Button(width // 2 - 100, height // 2, optionsImg, 0.8)  # Options button above Exit
end = Button(width // 2 - 100, height // 2 + 100, exitImg, 0.8)
pausebtn = Button(5, 5, pauseImg, 0.8)

# Load mute button image
muteImg = pygame.image.load("images/mute_btn.jpg")
muteBtn = Button(5, 50, muteImg, 0.8)  # Position the mute button at (5, 50)
is_muted = False  # Global variable to track mute state

# Function to reset apple group
def reset_apple_group():
    appleGroup.empty()
    for row in range(len(level1_data)):
        for column in range(len(level1_data[row])):
            if level1_data[row][column] == 6:  # 6 represents an apple in the level data
                apple = Apple(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                appleGroup.add(apple)

# Function to reset diamond group
def reset_daimond_group():
    daimondGroup.empty()
    for row in range(len(level1_data)):
        for column in range(len(level1_data[row])):
            if level1_data[row][column] == 7:  # 7 represents a diamond in the level data
                daimond = Daimond(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                daimondGroup.add(daimond)

# Similar functions for Level 2 and Level 3
def reset_apple_group2():
    appleGroup2.empty()
    for row in range(len(level2_data)):
        for column in range(len(level2_data[row])):
            if level2_data[row][column] == 8:  # 8 represents an apple in the level data
                apple2 = Apple(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                appleGroup2.add(apple2)

def reset_daimond_group2():
    daimondGroup2.empty()
    for row in range(len(level2_data)):
        for column in range(len(level2_data[row])):
            if level2_data[row][column] == 9:  # 9 represents a diamond in the level data
                daimond2 = Daimond(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                daimondGroup2.add(daimond2)

def reset_apple_group3():
    appleGroup3.empty()
    for row in range(len(level3_data)):
        for column in range(len(level3_data[row])):
            if level3_data[row][column] == 10:  # 10 represents an apple in the level data
                apple3 = Apple(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                appleGroup3.add(apple3)

def reset_daimond_group3():
    daimondGroup3.empty()
    for row in range(len(level3_data)):
        for column in range(len(level3_data[row])):
            if level3_data[row][column] == 11:  # 11 represents a diamond in the level data
                daimond3 = Daimond(column * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
                daimondGroup3.add(daimond3)

# Function to set resolution
def set_resolution(new_width, new_height):
    global width, height, screen, background, start, options, end, pausebtn, muteBtn
    width = new_width
    height = new_height
    screen = pygame.display.set_mode((width, height))
    if dark_mode:
        background = pygame.transform.scale(background_night, (width, height))
    else:
        background = pygame.transform.scale(background_day, (width, height))
    
    # Reinitialize buttons with new positions
    start = Button(width // 2 - 100, height // 2 - 100, startImg, 0.8)
    options = Button(width // 2 - 100, height // 2, optionsImg, 0.8)
    end = Button(width // 2 - 100, height // 2 + 100, exitImg, 0.8)
    pausebtn = Button(5, 5, pauseImg, 0.8)
    muteBtn = Button(5, 50, muteImg, 0.8)

# Options menu to change resolution, game mode, and theme
def optionsMenu():
    global width, height, screen, background, resolutions, game_modes, dark_mode, game_mode
    option = True
    selected_resolution = 0
    selected_mode = 0  # 0 for windowed, 1 for borderless, 2 for fullscreen
    selected_theme = 0  # 0 for light mode, 1 for dark mode
    selected_game_mode = 0  # 0 for walls, 1 for wrap-around

    while option:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_resolution = (selected_resolution - 1) % len(resolutions)
                if event.key == pygame.K_DOWN:
                    selected_resolution = (selected_resolution + 1) % len(resolutions)
                if event.key == pygame.K_LEFT:
                    selected_mode = (selected_mode - 1) % len(game_modes)
                if event.key == pygame.K_RIGHT:
                    selected_mode = (selected_mode + 1) % len(game_modes)
                if event.key == pygame.K_t:  # Press 'T' to toggle theme (dark/light mode)
                    selected_theme = (selected_theme + 1) % 2
                    dark_mode = not dark_mode
                    set_resolution(width, height)  # Update background image
                if event.key == pygame.K_g:  # Press 'G' to toggle game mode (walls/wrap-around)
                    selected_game_mode = (selected_game_mode + 1) % 2
                    game_mode = selected_game_mode
                if event.key == pygame.K_RETURN:
                    # Apply selected resolution and mode
                    new_width, new_height = resolutions[selected_resolution]
                    set_resolution(new_width, new_height)
                    if game_modes[selected_mode] == "Windowed":
                        screen = pygame.display.set_mode((new_width, new_height))
                    elif game_modes[selected_mode] == "Borderless":
                        screen = pygame.display.set_mode((new_width, new_height), pygame.NOFRAME)
                    elif game_modes[selected_mode] == "Fullscreen":
                        screen = pygame.display.set_mode((new_width, new_height), pygame.FULLSCREEN)
                    option = False

        screen.blit(background, (0, 0))  # Draw the current background
        largeText = pygame.font.SysFont("Elephant", 50)
        TextSurf, TextRect = TextThings("Options", largeText)
        TextRect.center = (width // 2, height // 4)
        screen.blit(TextSurf, TextRect)

        # Display resolution options
        for i, res in enumerate(resolutions):
            color = Highlight if i == selected_resolution else White
            res_text = f"{res[0]}x{res[1]}"
            TextSurf, TextRect = TextThings(res_text, largeText, color)
            TextRect.center = (width // 2, height // 2 + i * 50)
            screen.blit(TextSurf, TextRect)

        # Display game mode options
        mode_text = f"Mode: {game_modes[selected_mode]}"
        TextSurf, TextRect = TextThings(mode_text, largeText, Highlight if selected_mode == 0 else White)
        TextRect.center = (width // 2, height // 2 + len(resolutions) * 50)
        screen.blit(TextSurf, TextRect)

        # Display theme options
        theme_text = f"Theme: {'Dark Mode' if dark_mode else 'Light Mode'}"
        TextSurf, TextRect = TextThings(theme_text, largeText, Highlight if selected_theme == 0 else White)
        TextRect.center = (width // 2, height // 2 + (len(resolutions) + 1) * 50)
        screen.blit(TextSurf, TextRect)

        # Display game mode options (walls/wrap-around)
        game_mode_text = f"Game Mode: {'Walls' if game_mode == 0 else 'Wrap-around'}"
        TextSurf, TextRect = TextThings(game_mode_text, largeText, Highlight if selected_game_mode == 0 else White)
        TextRect.center = (width // 2, height // 2 + (len(resolutions) + 2) * 50)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)

# Game intro screen
def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))  # Draw the current background

        if start.draw():  # Start button
            gameLoop()
        if options.draw():  # Options button
            optionsMenu()
        if end.draw():  # Exit button
            click.play()
            time.sleep(0.2)
            gameQuit()
        if muteBtn.draw():  # Mute button
            global is_muted
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

        pygame.display.update()
        clock.tick(15)

# Unpause the game
def unpause():
    global pause
    pause = False

# Pause the game
def paused():
    largeText = pygame.font.SysFont("Elephant", 115)
    TextSurf, TextRect = TextThings("Paused", largeText)
    TextRect.center = (width // 2, height // 2)
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if start.draw():
            unpause()
        if end.draw():
            gameQuit()

        pygame.display.update()
        clock.tick(15)

# Quit the game
def gameQuit():
    pygame.quit()
    quit()

# Game over screen for Level 1
def gameOver():
    global appleCount, daimondCount
    appleCount = 0
    daimondCount = 0

    mainMusic.stop()
    gameOverMusic.play()
    mainMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("Game Over", largeText)
    TextRect.center = (width // 2, height // 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            gameLoop()
        if end.draw():
            click.play()
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

# Game over screen for Level 2
def gameOverLevel2():
    global appleCount, daimondCount
    appleCount = 0
    daimondCount = 0

    mainMusic.stop()
    gameOverMusic.play()
    mainMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("Game Over", largeText)
    TextRect.center = (width // 2, height // 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            gameLoop2()
        if end.draw():
            click.play()
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

# Game over screen for Level 3
def gameOverLevel3():
    global appleCount, daimondCount
    appleCount = 0
    daimondCount = 0

    mainMusic.stop()
    gameOverMusic.play()
    mainMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("Game Over", largeText)
    TextRect.center = (width // 2, height // 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            gameLoop3()
        if end.draw():
            click.play()
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

# Win screen
def win():
    mainMusic.stop()
    winMusic.play()

    largeText = pygame.font.SysFont("Elephant", 100)
    TextSurf, TextRect = TextThings("You won!", largeText)
    TextRect.center = (width // 2, height // 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)

        if start.draw():
            mainMusic.play()
            gameLoop()
        if end.draw():
            click.play()
            time.sleep(0.2)
            gameQuit()

        pygame.display.update()
        clock.tick(15)

# Function to respawn apples in No Border mode
def respawn_apple(apple_group, width, height, tile_size):
    apple_group.empty()  # Clear the existing apple
    # Generate a new random position for the apple
    row = random.randint(1, (height // tile_size) - 2)
    col = random.randint(1, (width // tile_size) - 2)
    apple = Apple(col * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
    apple_group.add(apple)

# Main game loop for Level 1
def gameLoop():
    global snakeHead, headRect, pause, snakeheadMask, appleCount, daimondCount, snake_length, level1_data, game_mode
    # Reset snake head direction, snake head mask, snake head position and other values
    snakeHead = snakeHeadDown
    snakeheadMask = pygame.mask.from_surface(snakeHead)
    headRect.topleft = (38, 38)
    direction = Vector2(0, 0)  # Initial direction is down
    hitCount = 0
    appleCount = 0
    daimondCount = 0
    snake_length = 1
    heartRect.topright = (width - 10, 5)
    heartRect2.topright = (width - 60, 5)
    heartRect3.topright = (width - 110, 5)
    snake_segments = [(38, 38)]
    reset_apple_group()  # Reset apples
    reset_daimond_group()  # Reset diamonds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                previous_position = headRect.topleft  # Update the previous position before moving
                if event.key == K_UP:  # Move the snake head
                    direction = Vector2(0, -20)
                    snakeHead = snakeHeadUp
                if event.key == K_DOWN:
                    direction = Vector2(0, 20)
                    snakeHead = snakeHeadDown
                if event.key == K_LEFT:
                    direction = Vector2(-20, 0)
                    snakeHead = snakeHeadLeft
                if event.key == K_RIGHT:
                    direction = Vector2(20, 0)
                    snakeHead = snakeHeadRight
                snakeheadMask = pygame.mask.from_surface(snakeHead)

        headRect.topleft += direction

        # Wrap-around logic for no walls mode
        if game_mode == 1:  # Wrap-around mode
            if headRect.left > width:
                headRect.right = 0
            elif headRect.right < 0:
                headRect.left = width
            if headRect.top > height:
                headRect.bottom = 0
            elif headRect.bottom < 0:
                headRect.top = height

        # Check for collisions with apples and diamonds
        if pygame.sprite.spritecollide(head_sprite, appleGroup, True):
            appleCount += 1
            good.play()
            snake_length += 1
            if game_mode == 1:  # Respawn apple in a new position in No Border mode
                respawn_apple(appleGroup, width, height, tile_size)

        if pygame.sprite.spritecollide(head_sprite, daimondGroup, True):
            daimondCount += 5
            good.play()
            snake_length += 5

        snake_segments.insert(0, headRect.topleft)

        # Remove the tail if the snake didn't grow
        if len(snake_segments) > snake_length:
            snake_segments.pop()

        # Check for self-collision (only in No Border mode)
        if game_mode == 1:
            for segment in snake_segments[1:]:  # Skip the head (first segment)
                if headRect.topleft == segment:  # If head collides with any body segment
                    lostLife.play()
                    time.sleep(0.5)
                    gameOver()
                    return

        # Check for win condition (only in walled mode)
        if game_mode == 0 and len(appleGroup) == 0 and len(daimondGroup) == 0:
            gameLoop2()  # Move to the next level
            return

        # Draw everything
        screen.blit(background, (0, 0))  # Draw the current background
        if game_mode == 0:  # Only draw obstacles in "Walls" mode
            level1.draw()
        pygame.draw.rect(screen, (255, 255, 255), headRect, 2)
        for segment in snake_segments:
            screen.blit(snakebody, segment)
        screen.blit(snakeHead, headRect)

        appleGroup.update()
        appleGroup.draw(screen)
        daimondGroup.update()
        daimondGroup.draw(screen)
        screen.blit(heart1, heartRect)
        screen.blit(heart2, heartRect2)
        screen.blit(heart3, heartRect3)
        ScoreText('Apples ' + str(appleCount), fontscore, Black, 100, 15)
        ScoreText('Diamonds ' + str(daimondCount), fontscore, Black, 200, 15)

        if pausebtn.draw():
            pause = True
            paused()

        if muteBtn.draw():  # Mute button
            global is_muted
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

        # Check for wall collisions (only in walled mode)
        if game_mode == 0 and level1.check_collision(headRect, snakeheadMask):
            lostLife.play()
            hitCount += 1
            headRect.topleft = previous_position
            if hitCount >= 3:
                time.sleep(0.5)
                gameOver()
                return

            if hitCount == 1:
                heartRect3.topleft = (-100, -100)
            elif hitCount == 2:
                heartRect2.topleft = (-100, -100)
            elif hitCount == 3:
                heartRect.topleft = (-100, -100)

        pygame.display.update()
        clock.tick(10)

# Main game loop for Level 2
def gameLoop2():
    global snakeHead, headRect, pause, snakeheadMask, bullet_active, bulletRect, snake_length, bulletMask, bullet_speed, width, game_mode
    # Reset snake head direction, snake head mask, snake head position and other things
    snakeHead = snakeHeadDown
    snakeheadMask = pygame.mask.from_surface(snakeHead)
    headRect.topleft = (38, 38)
    direction = Vector2(0, 0)  # Initial direction is down
    hitCount = 0
    appleCount = 0
    daimondCount = 0
    snake_length = 1
    heartRect.topright = (width - 10, 5)
    heartRect2.topright = (width - 60, 5)
    heartRect3.topright = (width - 110, 5)
    snake_segments = [(38, 38)]
    last_bullet_time = time.time()
    bullet_active = False
    bulletRect = pygame.Rect(soldier.get_rect().centerx, soldier.get_rect().centery, 10, 10)
    bulletMask = pygame.mask.from_surface(bulletImg)
    reset_apple_group2()
    reset_daimond_group2()

    print("Level 2 started!")  # Debug print

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                previous_position = headRect.topleft  # Update the previous position before moving
                if event.key == K_UP:  # Move the snake head
                    direction = Vector2(0, -20)
                    snakeHead = snakeHeadUp
                if event.key == K_DOWN:
                    direction = Vector2(0, 20)
                    snakeHead = snakeHeadDown
                if event.key == K_LEFT:
                    direction = Vector2(-20, 0)
                    snakeHead = snakeHeadLeft
                if event.key == K_RIGHT:
                    direction = Vector2(20, 0)
                    snakeHead = snakeHeadRight
                snakeheadMask = pygame.mask.from_surface(snakeHead)

        headRect.topleft += direction

        # Wrap-around logic for no walls mode
        if game_mode == 1:
            if headRect.left > width:
                headRect.right = 0
            elif headRect.right < 0:
                headRect.left = width
            if headRect.top > height:
                headRect.bottom = 0
            elif headRect.bottom < 0:
                headRect.top = height

        # Check for collisions with apples and diamonds
        if pygame.sprite.spritecollide(head_sprite, appleGroup2, True):
            appleCount += 1
            good.play()
            snake_length += 1
            if game_mode == 1:  # Respawn apple in a new position in No Border mode
                respawn_apple(appleGroup2, width, height, tile_size)

        if pygame.sprite.spritecollide(head_sprite, daimondGroup2, True):
            daimondCount += 5
            good.play()
            snake_length += 5

        snake_segments.insert(0, headRect.topleft)

        # Remove the tail if the snake didn't grow
        if len(snake_segments) > snake_length:
            snake_segments.pop()

        # Check for self-collision (only in No Border mode)
        if game_mode == 1:
            for segment in snake_segments[1:]:  # Skip the head (first segment)
                if headRect.topleft == segment:  # If head collides with any body segment
                    lostLife.play()
                    time.sleep(0.5)
                    gameOverLevel2()
                    return

        # Check for win condition (only in walled mode)
        if game_mode == 0 and len(appleGroup2) == 0 and len(daimondGroup2) == 0:
            print("Level 2 completed! Transitioning to Level 3...")  # Debug print
            gameLoop3()  # Move to the next level
            return

        # Draw everything
        screen.blit(background, (0, 0))  # Draw the current background
        if game_mode == 0:  # Only draw obstacles in "Walls" mode
            level2.draw()
        pygame.draw.rect(screen, (255, 255, 255), headRect, 2)
        for segment in snake_segments:
            screen.blit(snakebody, segment)
        screen.blit(snakeHead, headRect)
        appleGroup2.update()
        appleGroup2.draw(screen)
        daimondGroup2.update()
        daimondGroup2.draw(screen)
        screen.blit(heart1, heartRect)
        screen.blit(heart2, heartRect2)
        screen.blit(heart3, heartRect3)
        screen.blit(soldier, (575, 50))
        screen.blit(deadApple, deadAppleRect)
        ScoreText('Apples ' + str(appleCount), fontscore, Black, 100, 15)
        ScoreText('Diamonds ' + str(daimondCount), fontscore, Black, 200, 15)

        if bullet_active:
            # Calculate bullet direction
            target_x, target_y = 0, height  # Bottom-left corner of the screen
            dx = target_x - bulletRect.centerx
            dy = target_y - bulletRect.centery
            bullet_speed = 20
            # Normalize the direction vector
            length = (dx**2 + dy**2)**0.5
            dx /= length
            dy /= length
            bulletRect.x += bullet_speed * dx
            bulletRect.y += bullet_speed * dy
            if bulletRect.right < 0 or bulletRect.left > width or bulletRect.bottom < 0 or bulletRect.top > height:
                bullet_active = False
        else:
            current_time = time.time()
            if current_time - last_bullet_time > 6:  # Fire a bullet every wanted amount of seconds
                bullet_active = True
                bulletRect.center = (580, 118)
                last_bullet_time = current_time

        if bullet_active:
            screen.blit(bulletImg, bulletRect)

        # Check collision with bullet
        if bullet_active and snakeheadMask.overlap(bulletMask, (headRect.x - bulletRect.x, headRect.y - bulletRect.y)):
            lostLife.play()
            time.sleep(0.5)
            gameOverLevel2()
            return

        if pausebtn.draw():
            pause = True
            paused()

        if muteBtn.draw():  # Mute button
            global is_muted
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

        # Check for wall collisions (only in walled mode)
        if game_mode == 0 and level2.check_collision(headRect, snakeheadMask):
            lostLife.play()
            hitCount += 1
            headRect.topleft = previous_position
            if hitCount >= 3:
                time.sleep(0.9)
                gameOverLevel2()
                return

            if hitCount == 1:
                heartRect3.topleft = (-100, -100)
            elif hitCount == 2:
                heartRect2.topleft = (-100, -100)
            elif hitCount == 3:
                heartRect.topleft = (-100, -100)

        pygame.display.update()
        clock.tick(10)

# Main game loop for Level 3
def gameLoop3():
    global snakeHead, headRect, pause, snakeheadMask, appleCount, daimondCount, snake_length, level3_data, game_mode
    # Reset snake head direction, snake head mask, snake head position and other values
    snakeHead = snakeHeadDown
    snakeheadMask = pygame.mask.from_surface(snakeHead)
    headRect.topleft = (38, 38)
    direction = Vector2(0, 0)  # Initial direction is down
    hitCount = 0
    appleCount = 0
    daimondCount = 0
    snake_length = 1
    heartRect.topright = (width - 10, 5)
    heartRect2.topright = (width - 60, 5)
    heartRect3.topright = (width - 110, 5)
    snake_segments = [(38, 38)]
    reset_apple_group3()  # Reset apples
    reset_daimond_group3()  # Reset diamonds

    print("Level 3 started!")  # Debug print
    print(f"Apples in Level 3: {len(appleGroup3)}")  # Debug print
    print(f"Diamonds in Level 3: {len(daimondGroup3)}")  # Debug print

    while True:
        print("Game loop iteration started.")  # Debug print
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                print(f"Key pressed: {event.key}")  # Debug print
                previous_position = headRect.topleft  # Update the previous position before moving
                if event.key == K_UP:  # Move the snake head
                    direction = Vector2(0, -20)
                    snakeHead = snakeHeadUp
                if event.key == K_DOWN:
                    direction = Vector2(0, 20)
                    snakeHead = snakeHeadDown
                if event.key == K_LEFT:
                    direction = Vector2(-20, 0)
                    snakeHead = snakeHeadLeft
                if event.key == K_RIGHT:
                    direction = Vector2(20, 0)
                    snakeHead = snakeHeadRight
                snakeheadMask = pygame.mask.from_surface(snakeHead)

        headRect.topleft += direction

        # Wrap-around logic for no walls mode
        if game_mode == 1:  # Wrap-around mode
            if headRect.left > width:
                headRect.right = 0
            elif headRect.right < 0:
                headRect.left = width
            if headRect.top > height:
                headRect.bottom = 0
            elif headRect.bottom < 0:
                headRect.top = height

        # Check for collisions with apples and diamonds
        if pygame.sprite.spritecollide(head_sprite, appleGroup3, True):
            appleCount += 1
            good.play()
            snake_length += 1
            if game_mode == 1:  # Respawn apple in a new position in No Border mode
                respawn_apple(appleGroup3, width, height, tile_size)

        if pygame.sprite.spritecollide(head_sprite, daimondGroup3, True):
            daimondCount += 5
            good.play()
            snake_length += 5

        snake_segments.insert(0, headRect.topleft)

        # Remove the tail if the snake didn't grow
        if len(snake_segments) > snake_length:
            snake_segments.pop()

        # Check for self-collision (only in No Border mode)
        if game_mode == 1:
            for segment in snake_segments[1:]:  # Skip the head (first segment)
                if headRect.topleft == segment:  # If head collides with any body segment
                    lostLife.play()
                    time.sleep(0.5)
                    gameOverLevel3()
                    return

        # Check for win condition (only in walled mode)
        if game_mode == 0 and len(appleGroup3) == 0 and len(daimondGroup3) == 0:
            win()  # Player wins the game
            return

        # Draw everything
        print("Drawing Level 3 background...")  # Debug print
        screen.blit(background, (0, 0))  # Draw the current background

        if game_mode == 0:  # Only draw obstacles in "Walls" mode
            print("Drawing Level 3 obstacles...")  # Debug print
            level3.draw()

        print("Drawing snake...")  # Debug print
        pygame.draw.rect(screen, (255, 255, 255), headRect, 2)
        for segment in snake_segments:
            screen.blit(snakebody, segment)
        screen.blit(snakeHead, headRect)

        print("Drawing apples and diamonds...")  # Debug print
        appleGroup3.update()
        appleGroup3.draw(screen)
        daimondGroup3.update()
        daimondGroup3.draw(screen)

        print("Drawing hearts and score...")  # Debug print
        screen.blit(heart1, heartRect)
        screen.blit(heart2, heartRect2)
        screen.blit(heart3, heartRect3)
        ScoreText('Apples ' + str(appleCount), fontscore, Black, 100, 15)
        ScoreText('Diamonds ' + str(daimondCount), fontscore, Black, 200, 15)

        if pausebtn.draw():
            pause = True
            paused()

        if muteBtn.draw():  # Mute button
            global is_muted
            is_muted = not is_muted
            if is_muted:
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

        # Check for wall collisions (only in walled mode)
        if game_mode == 0 and level3.check_collision(headRect, snakeheadMask):
            lostLife.play()
            hitCount += 1
            headRect.topleft = previous_position
            if hitCount >= 3:
                time.sleep(0.5)
                gameOverLevel3()
                return

            if hitCount == 1:
                heartRect3.topleft = (-100, -100)
            elif hitCount == 2:
                heartRect2.topleft = (-100, -100)
            elif hitCount == 3:
                heartRect.topleft = (-100, -100)

        print("Updating display...")  # Debug print
        pygame.display.update()
        print(f"Game loop running at {clock.get_fps()} FPS")  # Debug print
        clock.tick(10)
# Call the game intro and start the game
gameIntro()
gameLoop()