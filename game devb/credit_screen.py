import pygame
from PIL import Image, ImageFilter

def control_screen():
    pygame.init()

    # Constants
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Warrior Legacy')

    # Load and blur background image
    pil_bg = Image.open("asset/background/fightbackround.jpg")
    blurred_bg = pil_bg.filter(ImageFilter.GaussianBlur(5))  # Apply Gaussian blur with radius 5
    background_img = pygame.image.fromstring(blurred_bg.tobytes(), blurred_bg.size, blurred_bg.mode)

    # Set FPS
    clock = pygame.time.Clock()
    FPS = 60

    # Load back button image
    back_btn_img = pygame.image.load("asset/Button/back.png").convert_alpha()
    back_btn_img = pygame.transform.scale(back_btn_img, (200, 50))
    back_rect = back_btn_img.get_rect(center=(SCREEN_WIDTH // 2, 650))

    # Fonts
    menu_font = pygame.font.Font(None, 74)
    control_font = pygame.font.Font(None, 25)  # Smaller font size for controls

    # Control screen loop
    run_control = True
    while run_control:
        # Get the current screen size
        current_width, current_height = screen.get_size()

        # Scale the background to fit the current screen size
        scaled_bg = pygame.transform.scale(background_img, (current_width, current_height))
        screen.blit(scaled_bg, (0, 0))  # Draw the scaled background

        # Render title and back button
        control_title_text = menu_font.render('Controls', True, BLACK)
        screen.blit(control_title_text, (current_width // 2 - control_title_text.get_width() // 2, 100))

        back_rect = back_btn_img.get_rect(center=(current_width // 2, current_height - 70))  # Adjust position dynamically
        screen.blit(back_btn_img, back_rect)

        # Control instructions
        player1_controls = [
            "PLAYER 1 CONTROLS",
            "D = MOVE PLAYER FORWARD",
            "A = MOVE PLAYER BACKWARD",
            "W = JUMP",
            "C = ATTACK 1",
            "V = ATTACK 2",
        ]

        player2_controls = [
            "PLAYER 2 CONTROLS",
            "LEFT ARROW       = MOVE PLAYER FORWARD",
            "RIGHT ARROW    = MOVE PLAYER BACKWARD",
            "UP ARROW          = JUMP",
            "Numkey 2             = ATTACK 1",
            "Numkey 3             = ATTACK 2",
        ]

        # Render control instructions
        for i, line in enumerate(player1_controls):
            control_text = control_font.render(line, True, BLACK)
            screen.blit(control_text, (50, 200 + i * 40))  # Adjust position for dynamic screen size

        for i, line in enumerate(player2_controls):
            control_text = control_font.render(line, True, BLACK)
            screen.blit(control_text, (current_width // 2 + 50, 200 + i * 40))  # Adjust position for dynamic screen size

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_control = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if back_rect.collidepoint(event.pos):  # Check if "back" button is clicked
                        run_control = False
            if event.type == pygame.VIDEORESIZE:  # Handle window resize
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    control_screen()
