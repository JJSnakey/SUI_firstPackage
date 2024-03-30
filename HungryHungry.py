import pygame
import sys
import random

#===========================================================================================================================
#Pre game

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH = 1400
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUI Hungry Hungry Alligators")

# Load the background image
background_image = pygame.image.load("landscape.png").convert()

# Set up colors
WHITE =  (255,255,255)
BLACK = (0, 0, 0)

#===========================================================================================================================
#game objects

# Set up the player (square)
class Player:
    def __init__(self, x, y, size=50, speed=5):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self):
        pygame.draw.rect(window, BLACK, self.rect)

#object to be eaten
class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
    
    def draw(self):
        pygame.draw.circle(window, WHITE, (self.x, self.y), self.radius)

#===========================================================================================================================
#game functions

#determine if colliding
def is_collision(obj1, obj2):
    distance = ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5
    if distance < (obj1.radius) + (obj2.size / 2):
        return True
    return False

#===========================================================================================================================
#initialization

# Create player
player = Player(WIDTH // 2 - 25, HEIGHT // 2 - 25)

# Create white circles
circles = []
for _ in range(5):
    circle = Circle(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
    circles.append(circle)

#===========================================================================================================================

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check for collision with white circles and remove them
                for circle in circles:
                    if is_collision(circle, player):
                        circles.remove(circle)
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] | keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT] | keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_UP] | keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_DOWN] | keys[pygame.K_s]:
        player.move(0, 1)
    
    # Blit the background image onto the window
    window.blit(background_image, (0, 0))

    # Draw the square
    player.draw()

    # Draw white circles
    for circle in circles:
        circle.draw()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    pygame.time.Clock().tick(20)

#===========================================================================================================================

# Quit Pygame
pygame.quit()
sys.exit()