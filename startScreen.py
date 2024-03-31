import pygame
import sys
import pygame.locals as pl

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Window")

background_image = pygame.image.load("startLoad.png").convert()
# Fill the background
screen.blit(background_image, (0,0))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 32)

## Textbox class
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

# Create textboxes
textbox1 = TextBox(150, 100, 400, 50)
textbox2 = TextBox(150, 200, 400, 50)

text_boxes = [textbox1, textbox2]

# Main loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for textbox in text_boxes:
            textbox.handle_event(event)


    # Draw textboxes
    for textbox in text_boxes:
        textbox.draw(screen)

    pygame.display.flip()