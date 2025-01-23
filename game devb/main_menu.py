import pygame
import sys
from credit_screen import control_screen  # Import function credit_screen
from pygame import mixer

mixer.init()
pygame.init()

# icon game
icon = pygame.image.load("asset/icon/icon.png")
pygame.display.set_icon(icon)

# game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Warrior Legacy')

# set fps
clock = pygame.time.Clock()
FPS = 60

#contnast
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BORDER_COLOR = (255, 0, 0)  # Border color 
FONT_PATH = 'asset/font/FFF_Tusj.ttf'  # Update with the path to your font file
BACKGROUND_PATH = 'asset/background/fightbackround.jpg'  # Path to your background image


# Load and scale button images
start_btn_img = pygame.image.load("asset/Button/play.png").convert_alpha()
start_btn_img = pygame.transform.scale(start_btn_img, (200, 50))  # Scale for resume button
control_btn_img = pygame.image.load("asset/Button/control.png").convert_alpha()
control_btn_img = pygame.transform.scale(control_btn_img, (200, 50))  # Scale for back to menu button
quit_btn_img = pygame.image.load("asset/Button/quit.png").convert_alpha()
quit_btn_img = pygame.transform.scale(quit_btn_img, (200, 50))  

# Load background image
background = pygame.image.load("asset/background/fightbackround.jpg").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and play background music
pygame.mixer.music.load("asset/music/fight song.wav")  # Ensure you load a valid music file
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Utility function to render text with border
def render_text_with_border(font, text, color, border_color):
    # Create base text surface
    base_text = font.render(text, True, color)
    
    # Create a new surface with size a bit larger than the base text
    text_surface = pygame.Surface((base_text.get_width() + 2, base_text.get_height() + 2), pygame.SRCALPHA)
    
    # Fill the text surface with transparency
    text_surface.fill((0, 0, 0, 0))
    
    # Render the border text by blitting the base text multiple times with offsets
    border_text = font.render(text, True, border_color)
    text_surface.blit(border_text, (0, 1))
    text_surface.blit(border_text, (2, 1))
    text_surface.blit(border_text, (1, 0))
    text_surface.blit(border_text, (1, 2))
    text_surface.blit(border_text, (2, 2))
    text_surface.blit(border_text, (0, 0))
    text_surface.blit(border_text, (0, 2))
    text_surface.blit(border_text, (2, 0))
    text_surface.blit(border_text, (2, 2))
    
    # Blit the base text over the border
    text_surface.blit(base_text, (1, 1))
    
    return text_surface

# Main menu function
def main_menu():
    title_font = pygame.font.Font(FONT_PATH, 74)  # Load custom font for title
    menu_font = pygame.font.Font(None, 74)  # Default font for other menu items
    run_menu = True

    # Define button rectangles for detection
    start_btn_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 300, 200, 50))
    control_btn_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 380, 200, 50))
    quit_btn_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, 450, 200, 50))

    while run_menu:
        screen.blit(background, (0, 0))  # Draw background image
        title_text = render_text_with_border(title_font, 'Warrior Legacy', WHITE, BORDER_COLOR)
        
        # Draw buttons
        screen.blit(start_btn_img, start_btn_rect.topleft)
        screen.blit(control_btn_img, control_btn_rect.topleft)
        screen.blit(quit_btn_img, quit_btn_rect.topleft)
        
        # Draw title text
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_btn_rect.collidepoint(event.pos):
                        run_menu = False
                    elif control_btn_rect.collidepoint(event.pos):
                        control_screen()  # Call control_screen function
                    elif quit_btn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()
