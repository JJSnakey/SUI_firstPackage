import pygame
import sys
import random
import math

#===========================================================================================================================
#Pre game

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH = 1400
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUI Hungry Hungry Alligators")

# Load the images
background_image = pygame.image.load("landscape.png").convert()
player_image = pygame.image.load("arrow.png").convert_alpha()
fish_image = pygame.image.load("fish.png").convert_alpha()

# Set up colors
WHITE =  (255,255,255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)

#===========================================================================================================================
#game objects

# Set up the player (square)
class Player:
    def __init__(self, x, y, size=50, speed=5, score=0):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.score = score
        self.image = pygame.transform.scale(player_image, (size, size))  # Scale the image to match the player size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self):
        window.blit(self.image, self.rect)

    def crunch(fishes, self):
        for fish in fishes:
            if is_collision(fish, self):
                fishes.remove(fish)
                self.score += 1

#area for fishes to spawn
class Pond:
    def __init__(self, x, y, radius = 350):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        
    def is_inside(self, x, y):
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.radius

    def draw(self):
        pygame.draw.circle(window, BLUE, (self.x, self.y), self.radius, 2)

#object to be eaten (eating a fish counts score, zero fish left ends the game)
class Fish:
    def __init__(self, x, y, radius=20, speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0.5,0.5), (-0.5,0.5), (-0.5,-0.5), (0.5,-0.5)])  # Random initial direction
        self.dx, self.dy = self.direction
        self.original_image = pygame.transform.scale(fish_image, (self.radius+10, self.radius+10))  # Scale the image to match the player size
        self.image = self.original_image
        self.angle = 0

    def rotate(self):
        # Calculate the angle of rotation based on the direction
        self.angle = -math.degrees(math.atan2(self.dy, self.dx)+2.19)
        self.image = pygame.transform.rotate(self.original_image, int(self.angle))
    
    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        
        # Check if the fish hits the pond boundaries, change direction if it does
        if not pond.rect.colliderect(self.rect):
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self):
        self.rotate()
        window.blit(self.image, self.rect)
        #pygame.draw.circle(window, WHITE, (self.x, self.y), self.radius)

#===========================================================================================================================
#game functions

def display_score(score, posX, posY):
    font = pygame.font.Font(None, 36)  # Choose a font and font size
    text = font.render("Score: " + str(score), True, WHITE)  # Render the score text
    window.blit(text, (posX, posY))  # Blit the text onto the game window at posX,posY

#determine if fish spawned in the pond      //used for spawn
def is_inside_pond(x, y, pond):
    distance = ((x - pond.x)**2 + (y - pond.y)**2)**0.5
    if distance < pond.radius:
        return True
    return False

#determine if colliding
def is_collision(obj1, obj2):               #obj1 fish, obj2 player
     # Calculate the center coordinates of obj1
    obj1_center_x = obj1.x + obj1.radius
    obj1_center_y = obj1.y + obj1.radius

    # Calculate the center coordinates of obj2
    obj2_center_x = obj2.x + obj2.size
    obj2_center_y = obj2.y + obj2.size

    # Calculate the distance between the centers of the two objects
    distance = ((obj1_center_x - obj2_center_x)**2 + (obj1_center_y - obj2_center_y)**2)**0.5

    # Compare the distance with the sum of the radii to check for collision
    if distance < obj1.radius + obj2.size / 2 - 20:     #adjusted for more accurate visual calc
        return True
    return False

#===========================================================================================================================
#initialization

# Create players
player = Player(WIDTH // 2 - 125, HEIGHT // 2 - 25)
player2 = Player(WIDTH // 2 + 75, HEIGHT // 2 - 25)

#Create play zone (pond)
pond = Pond(700, 400)       #hardcoded wtih radius 350, at location 700,400 (the center)

# Create fishes
fishes = []
for i in range(50):
    x = random.randint(400, 800)
    y = random.randint(100, 700)
    while not is_inside_pond(x, y, pond):
        x = random.randint(400, 800)
        y = random.randint(100, 700)
    fish = Fish(x, y)
    fishes.append(fish)


#===========================================================================================================================

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    #player
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)
    if keys[pygame.K_SPACE]:
        player.crunch(fishes)   #passes 2 arguments, player and fishes

    #player2
    if keys[pygame.K_LEFT]:
        player2.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player2.move(1, 0)
    if keys[pygame.K_UP]:
        player2.move(0, -1)
    if keys[pygame.K_DOWN]:
        player2.move(0, 1)
    if keys[pygame.K_PERIOD]:
        player2.crunch(fishes)   #passes 2 arguments, player2 and fishes
    
    # Drawing------
    window.blit(background_image, (0, 0))
    display_score(player.score, 10, 10)
    display_score(player2.score, 10, 40)

    pond.draw()  #draw the pond (remove later)
    player.draw()
    player2.draw()
    for fish in fishes:
        fish.move()
        if not pond.is_inside(fish.x, fish.y):  #turn that puppy around
            fish.dx = -fish.dx
            fish.dy = -fish.dy
        fish.draw()
    
    # Update the  display
    pygame.display.flip()
    
    # Cap the frame rate
    pygame.time.Clock().tick(20)

#===========================================================================================================================
#game end

    # Check if all fishes are eaten
    if len(fishes) == 0:
        running = False  # End the game if no more fishes left

#===========================================================================================================================

# Quit Pygame
pygame.quit()
sys.exit()