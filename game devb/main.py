import pygame
from pygame import mixer
from fighter import Fighter
from main_menu import main_menu
from PIL import Image
import os

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

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player score
round_over = False
FIGHT_DURATION = 60000      # 60 seconds in milliseconds
fight_start_time = None
ROUND_OVER_COOLDOWN = 2000
fight_display_duration = 1000  # Duration to display "Fight!" in milliseconds
fight_display_time = None
paused = False

# fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 4
WIZARD_OFFSET = [90, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sound effects
pygame.mixer.music.load("asset/music/fight song.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# load sound effects
sword_fx = pygame.mixer.Sound("asset/music/warrior.wav")
sword_fx.set_volume(0.5)
wizard_fx = pygame.mixer.Sound("asset/music/wizard.mp3")
wizard_fx.set_volume(0.5)

# Pisahkan GIF menjadi frame-frame (ini hanya perlu dijalankan sekali sebelum game dimulai)
gif = Image.open('asset/background/battlearena.gif')
if not os.path.exists('frames'):
    os.makedirs('frames')
for frame in range(0, gif.n_frames):
    gif.seek(frame)
    gif.save(f'frames/frame_{frame}.png')

# Muat frame-frame
background_frames = []
for frame in os.listdir('frames'):
    background_frames.append(pygame.image.load(f'frames/{frame}'))

# Variabel untuk mengatur frame saat ini
frame_index = 0

# Durasi frame dalam milidetik
FRAME_DURATION = 100  # Sesuaikan sesuai kebutuhanmu
last_frame_update = pygame.time.get_ticks()

# load Warrior Spritesheet
warrior_sheet = pygame.image.load('asset/animation/warrior/sprites/warrior.png').convert_alpha()

# load Wizard Spritesheet
wizard_sheet = pygame.image.load('asset/animation/wizard/wizard.png').convert_alpha()

# define number of steps in animations
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 8, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

main_menu()

# load fonts
count_font = pygame.font.Font("asset/font/rough.ttf", 80)
score_font = pygame.font.Font("asset/font/antonio.ttf", 30)
winner_font = pygame.font.Font("asset/font/Cabai.ttf", 74)  # Load a specific font for winner text
menu_font = pygame.font.Font("asset/font/antonio.ttf", 50)

# Load and scale button images
resume_btn_img = pygame.image.load("asset/Button/resume.png").convert_alpha()
resume_btn_img = pygame.transform.scale(resume_btn_img, (200, 50))  # Scale for resume button
menu_btn_img = pygame.image.load("asset/Button/menu.png").convert_alpha()
menu_btn_img = pygame.transform.scale(menu_btn_img, (200, 50))  # Scale for back to menu button
restart_btn_img = pygame.image.load("asset/Button/restart.png").convert_alpha()
restart_btn_img = pygame.transform.scale(restart_btn_img, (200, 50))  # Scale for restart button

# Draw button function with centered positioning
def draw_button(image, x, y):
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect.topleft)
    return rect

# Draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    global frame_index, last_frame_update
    if pygame.time.get_ticks() - last_frame_update >= FRAME_DURATION:
        frame_index = (frame_index + 1) % len(background_frames)
        last_frame_update = pygame.time.get_ticks()
    scaled_bg = pygame.transform.scale(background_frames[frame_index], (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# health bar
def draw_health_bar(screen, health, x, y):
    bar_width = 400
    bar_height = 15
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 1, y - 1, bar_width + 2, bar_height + 2))
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * ratio, bar_height))

# energy bar
def draw_energy_bar(screen, energy, x, y):
    bar_width = 400
    bar_height = 15
    ratio = energy / 100
    pygame.draw.rect(screen, WHITE, (x - 1, y + bar_height + 9, bar_width + 2, bar_height + 2))
    pygame.draw.rect(screen, RED, (x, y + bar_height + 10, bar_width, bar_height))
    pygame.draw.rect(screen, BLUE, (x, y + bar_height + 10, bar_width * ratio, bar_height))

# create two instances of fighter
fighter_1 = Fighter(1, 300, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 800, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)

# game loop
run = True
while run:
    clock.tick(FPS)

    # draw background
    draw_bg()

    if paused:
        # Draw the pause menu
        draw_text("PAUSED", menu_font, BLACK, SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 3 - 20)
        
        # Draw resume button
        resume_button_rect = draw_button(resume_btn_img, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30)
        
        # Draw menu button
        menu_button_rect = draw_button(menu_btn_img, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30)

        # event handler for pause menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if resume_button_rect.collidepoint(mx, my):
                    paused = False
                if menu_button_rect.collidepoint(mx, my):
                    main_menu()
                    run = False

        # event handler for main menu
    else:
        # show player health and energy
        draw_health_bar(screen, fighter_1.health, 20, 20)
        draw_health_bar(screen, fighter_2.health, 850, 20)
        draw_energy_bar(screen, fighter_1.energy, 20, 35)
        draw_energy_bar(screen, fighter_2.energy, 850, 35)
        draw_text("Mystic Warrior:" + str(score[0]), score_font, RED, 30, 100)
        draw_text("Dark Sorcerer:" + str(score[1]), score_font, RED, 860, 100)
        
        # Update Countdown
        if intro_count <= 0:
            if fight_display_time is None:
                fight_display_time = pygame.time.get_ticks()
            
            if (pygame.time.get_ticks() - fight_display_time) < fight_display_duration:
                draw_text("Fight!", count_font, RED, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 3)
            else:
                # move fighters
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
        else:
            # display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # Update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # update fighter images
        fighter_1.update()
        fighter_2.update()

        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Check player defeat
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                winner_text = "Dark Sorcerer Wins!"
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                winner_text = "Mystic Warrior Wins!"
        
        # Display winner text if the round is over
        if round_over:
            draw_text(winner_text, winner_font, RED, SCREEN_WIDTH / 2 - 350, SCREEN_HEIGHT / 4)

            # Draw restart and menu buttons
            restart_button_rect = draw_button(restart_btn_img, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            menu_button_rect = draw_button(menu_btn_img, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60)

            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if restart_button_rect.collidepoint(mx, my):
                            round_over = False
                            intro_count = 3
                            fighter_1 = Fighter(1, 300, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                            fighter_2 = Fighter(2, 800, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)
                        if menu_button_rect.collidepoint(mx, my):
                            main_menu()
                            run = False

        # event handler for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

    # update display
    pygame.display.update()

pygame.quit()
