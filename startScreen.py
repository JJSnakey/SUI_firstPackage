import pygame
import sys
import pygame.locals as pl
import subprocess
#import HungryHungry

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Window")

background_image = pygame.image.load("startLoad.png").convert()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


# Font=================================================================================
font = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 100)
font3 = pygame.font.Font(None, 50)

# Fill the background
screen.blit(background_image, (0,0))

text = font2.render("HUNGRY HUNGRY ALLIGATORS", True, BLACK)
text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 100))
screen.blit(text, text_rect)

text = font3.render("Children's Crypto Gambling Game", True, BLACK)
text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 170))
screen.blit(text, text_rect)

text = font3.render("Wallet Player 1:", True, BLACK)
text_rect = text.get_rect(center=(145, 325))
screen.blit(text, text_rect)

text = font3.render("Wallet Player 2:", True, BLACK)
text_rect = text.get_rect(center=(145, 425))
screen.blit(text, text_rect)

## Textbox class============================================================================================
class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the textbox
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the active color
            self.color = BLACK if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Process the input when Enter is pressed
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.text = self.text[:-1]
                elif event.key == pygame.K_v and pygame.key.get_mods() & pl.KMOD_CTRL:
                    # Handle Ctrl+V to paste text from clipboard
                    clipboard_text = pygame.scrap.get(pl.SCRAP_TEXT).decode('utf-8')
                    self.text += clipboard_text
                else:
                    # Add typed character to the text
                    self.text += event.unicode

    def draw(self, screen):
        # Draw the textbox
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Render the text surface
        txt_surface = font.render(self.text, True, BLACK)
        # Blit the text surface to the screen
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

#==========================================================================================================================
        
class Button:
    def __init__(self, x, y, width, height, text, button_color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        start_game()

def start_game():
    subprocess.Popen(["python", "HungryHungry.py"])
    

# Create textboxes and buttons===================================================================================================
textbox1 = TextBox(300, 300, 500, 50)
textbox2 = TextBox(300, 400, 500, 50)

text_boxes = [textbox1, textbox2]

start_button = Button(SCREEN_WIDTH//2 - 100, 600, 200, 50, "Start Game", BLACK, WHITE)

# Main loop===============================================================================================================================================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for textbox in text_boxes:
            textbox.handle_event(event)


    # Draw textboxes and button
    for textbox in text_boxes:
        textbox.draw(screen)
    
    start_button.draw(screen)

    pygame.display.flip()