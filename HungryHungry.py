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
player_image = pygame.image.load("crocodile.png").convert_alpha()
fish_image = pygame.image.load("fish.png").convert_alpha()

# Set up colors
WHITE =  (255,255,255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)

#===========================================================================================================================
#game objects

# Set up the player (square)
class Player:
    def __init__(self, x, y, angle, size=50, speed=5, score=0):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.score = score
        self.angle = angle
        self.original_image = pygame.transform.scale(player_image, (size+50, size+50))  # Scale the image to match the player size
        self.image = self.original_image
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def turn_left(self):
        self.angle += 3  # Adjust the turning angle

    def turn_right(self):
        self.angle -= 3  # Adjust the turning angle      

    def move_forward(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = -self.speed * math.sin(math.radians(self.angle))
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
    
    def draw(self):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, new_rect)

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
    def __init__(self, x, y, radius=30, speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0.5,0.5), (-0.5,0.5), (-0.5,-0.5), (0.5,-0.5)])  # Random initial direction
        self.dx, self.dy = self.direction
        self.original_image = pygame.transform.scale(fish_image, (30,30))  # Scale the image to match the player size
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
    text = font.render("Score: " + str(score), True, BLACK)  # Render the score text
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

def display_winner(player1_score, player2_score):
    winner = "Player 1" if player1_score > player2_score else "Player 2" if player2_score > player1_score else "It's a tie!"
    font = pygame.font.Font(None, 72)  # Choose a font and font size
    text = font.render(f"{winner} wins!", True, BLACK)  # Render the winner text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(text, text_rect)

    text = font.render(f"20 SUI has been added to {winner}'s wallet", True, BLACK)  # Render the winner text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    window.blit(text, text_rect)

    pygame.display.flip()
    pygame.time.delay(10000)  # Display winner for 30 seconds before quitting

#===========================================================================================================================
#initialization

# Create players
players = []
player1 = Player(WIDTH // 2 - 225, HEIGHT // 2 - 25, 0)     #posX,posY,angle
players.append(player1)
player2 = Player(WIDTH // 2 + 175, HEIGHT // 2 - 25, 180)
players.append(player2)

#Create play zone (pond)
pond = Pond(700, 400)       #hardcoded wtih radius 350, at location 700,400 (the center)

# Create fishes
fishes = []
for i in range(1):
    x = random.randint(400, 1200)
    y = random.randint(100, 700)
    while not is_inside_pond(x, y, pond):
        x = random.randint(400, 800)
        y = random.randint(100, 700)
    fish = Fish(x, y)
    fishes.append(fish)


#===========================================================================================================================

# Main game loop
running = True
#gameBegin = False
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    #player1
    if keys[pygame.K_a]:
        player1.turn_left()
    if keys[pygame.K_d]:
        player1.turn_right()
    if keys[pygame.K_w]:
        player1.move_forward()

    #player2
    if keys[pygame.K_j]:
        player2.turn_left()
    if keys[pygame.K_l]:
        player2.turn_right()
    if keys[pygame.K_i]:
        player2.move_forward()

    for fish in fishes:
            if is_collision(fish, player1):
                fishes.remove(fish)
                player1.score += 1
            elif is_collision(fish, player2):
                fishes.remove(fish)
                player2.score += 1

    # Drawing------
    window.blit(background_image, (0, 0))
    display_score(player1.score, 10, 10)
    display_score(player2.score, 10, 40)

    player1.draw()
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
        display_winner(player1.score, player2.score)
        running = False

#===========================================================================================================================

# Quit Pygame
pygame.quit()
sys.exit()