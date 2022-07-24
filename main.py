import sys
import pygame
import random
from pygame import mixer

pygame.init()

# Game Font
game_font = pygame.font.Font('04B_19.TTF', 40)

# Window
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('Assets/redbird-midflap.png'))

background_surface = pygame.image.load('Assets/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

base_surface = pygame.image.load('Assets/base.png').convert()
base_surface = pygame.transform.scale2x(base_surface)
base_position = 0

window = pygame.transform.scale2x(pygame.image.load('Assets/message.png').convert_alpha())
window_rect = window.get_rect(center=(288, 512))

game_over = pygame.transform.scale2x(pygame.image.load('Assets/gameover.png').convert_alpha())

clock = pygame.time.Clock()

# Bird
bird_downflap = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRDANIMATIONS = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDANIMATIONS, 100)
gravity = 0.25
bird_movement = 0

# Pipes
pipe_surface = pygame.image.load('Assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPES = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPES, 1200)
pipe_height = [400, 600, 800]
pipe_flip = pygame.transform.flip(pipe_surface, False, True)

# Score
score = 0
high_score = 0
score_sound = mixer.Sound('Sounds/sound_sfx_point.wav')

# Game Running
game_active = True
start = False


def base_display():
    screen.blit(base_surface, (base_position, 900))
    screen.blit(base_surface, (base_position + 576, 900))


def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    # Creates two pipes
    new_pipe_bottom = pipe_surface.get_rect(midtop=(700, random_pipe_height))
    new_pipe_top = pipe_surface.get_rect(midbottom=(700, random_pipe_height - 300))
    return new_pipe_bottom, new_pipe_top


def pipe_move(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def pipe_display(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            screen.blit(pipe_flip, pipe)


def check_collision(pipes):
    death_sound = mixer.Sound('Sounds/sound_sfx_hit.wav')
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return True
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        return True
    return False


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game):
    if game == 'game running':
        score_render = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        screen.blit(score_render, (190, 100))
    else:
        screen.blit(window, window_rect)
        screen.blit(game_over, (100, 50))
        score_render = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        screen.blit(score_render, (185, 800))
        high_score_render = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 255))
        screen.blit(high_score_render, (135, 850))


def high_score_update(recent, high):
    if recent > high:
        high = recent
    return high


running = True
# Main game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                start = True
                bird_movement = 0
                bird_movement -= 10  # Bird Jump Height
                flap_sound = mixer.Sound('Sounds/sound_sfx_wing.wav')
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                bird_rect.center = (100, 250)
                pipe_list.clear()
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPES:
            if game_active and start:
                pipe_list.extend(create_pipe())
        if event.type == BIRDANIMATIONS:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(background_surface, (0, 0))
    if not start:
        screen.blit(window, window_rect)
        creator = game_font.render('DEVELOPED BY SANDIP BASAK', True, (255, 255, 255))
        screen.blit(creator, (25, 800))
        pygame.display.update()
        continue
    if game_active:
        # Score increment
        score += 0.25
        if int(score % 100) == 0 and score > 1:
            score_sound.play()

        # Pipes Movement
        pipe_list = pipe_move(pipe_list)
        pipe_display(pipe_list)

        # Bird Movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Collision Check
        if check_collision(pipe_list):
            game_active = False

    high_score = high_score_update(score, high_score)

    # Floor
    base_position -= 2
    base_display()
    if base_position < -576:
        base_position = 0

    if game_active:
        score_display('game running')
    else:
        score_display('game over')

    # Display Update
    pygame.display.update()
    clock.tick(120)
