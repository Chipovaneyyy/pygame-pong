import pygame, sys
from pygame.locals import *
import pygame.freetype
from random import randint

def draw_paddle(window, paddle_color, x, y, width, height):
    pygame.draw.rect(window, paddle_color, (x, y, width, height))

def draw_ball(x, y):
    global window
    pygame.draw.circle(window, (255, 255, 255), (x, y), 5)

def check_collision():
    global ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y, ball_velocity_x, ball_velocity_y
    global y_left, y_right, paddle_height, paddle_width
    
    #vertical check
    if ball_pos_y <= 5 or ball_pos_y >= 495:
        ball_direction_y *= -1
    
    # horizontal check
    # right check
    if ball_pos_x >= 500 - paddle_width - 10:
        if ball_pos_y >= y_right and ball_pos_y <= y_right + paddle_height:
            ball_direction_x *= -1
            ball_velocity_y = randint(-5, 5)
    # left check
    if ball_pos_x <= 0 + paddle_width + 10:
        if ball_pos_y >= y_left and ball_pos_y <= y_left + paddle_height:
            ball_direction_x *= -1
            ball_velocity_y = randint(-5, 5)

def check_score(ball_pos_x):
    global score_left, score_right
    if ball_pos_x > 500:
        score_left += 1
        return True
    elif ball_pos_x < 0:
        score_right += 1
        return True
    return False

pygame.init()

size = width,height = 500,500
bg_color = (0,0,0)
title = "Pong"

window = pygame.display.set_mode(size)
pygame.display.set_caption(title)

# ball
ball_pos_x = 250
ball_pos_y = 250
ball_velocity_x = 5
ball_velocity_y = 0
ball_direction_x = 1      # 1 or -1
ball_direction_y = 1
draw_ball(ball_pos_x, ball_pos_y)

# paddle properties
vel = 10
paddle_color = (255, 255, 255)
paddle_width = 10
paddle_height = 100
    # left paddle
y_left = 200
draw_paddle(window, paddle_color, 10, y_left, paddle_width, paddle_height)
    # right paddle
y_right = 200
draw_paddle(window, paddle_color, 480, y_right, paddle_width, paddle_height)

# score
font = pygame.font.Font("FreeSansBold.ttf", 32)
score_left = score_right = 0
draw_score_left = font.render(str(score_left), True, paddle_color)
draw_score_right = font.render(str(score_right), True, paddle_color)

running = True
while running:
    pygame.time.delay(30)
    keys = pygame.key.get_pressed()

    # i want to die
    for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

     # move left
    if keys[ord("w")] and y_left >= 0:
        y_left -= vel
    if keys[ord("s")] and y_left <= 500 - paddle_height:
        y_left += vel

    # move right
    if keys[pygame.K_UP] and y_right >= 0:
        y_right -= vel
    if keys[pygame.K_DOWN] and y_right <= 500 - paddle_height:
        y_right += vel

    # move ball
    ball_pos_x += ball_velocity_x * ball_direction_x
    ball_pos_y += ball_velocity_y * ball_direction_y
    check_collision()

    # score
    if check_score(ball_pos_x):
        ball_pos_x = 250
        ball_pos_y = 250
        ball_velocity_x = randint(-5, 5)
        while ball_velocity_x == 0:
            ball_velocity_x = randint(-5, 5)
        ball_velocity_y = 0
        ball_direction_x = 1
        ball_direction_y = 1

    # update frame
    window.fill(bg_color)
        # move ball
    draw_ball(ball_pos_x, ball_pos_y)
        # move left
    draw_paddle(window, paddle_color, 10, y_left, paddle_width, paddle_height)
        # move right
    draw_paddle(window, paddle_color, 480, y_right, paddle_width, paddle_height)
        # draw score
    draw_score_left = font.render(str(score_left), True, paddle_color)
    draw_score_right = font.render(str(score_right), True, paddle_color)
    window.blit(draw_score_left, (225, 25))
    window.blit(draw_score_right, (275, 25))

    pygame.display.update()
