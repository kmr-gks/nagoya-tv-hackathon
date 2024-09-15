import pygame
from pygame.locals import *
import random
import sys

# Pygameを初期化
pygame.init()

# ウィンドウの設定
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# 色の設定
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

def main():
    
    px=250
    py=300

    ex=250
    ey=0
    
    man = pygame.image.load("image\\syougakusei.png")
    man = pygame.transform.scale(man,(100,100))
    man_rect = pygame.Rect(250, 300, 100, 100)

    oct = pygame.image.load("image\\utyuujin.png")
    oct = pygame.transform.scale(oct,(100,100))

    ball_diameter = 30
    ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, screen_height // 2 - ball_diameter // 2, ball_diameter, ball_diameter)
    ball_speed_x = 3 * random.choice((1, -1))
    ball_speed_y = 3 * random.choice((1, -1))

    while True:
         
        screen.fill(white)
        screen.blit(man,(px,py))
        screen.blit(oct,(ex,ey))

        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys =pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and px>0:
            px -= 5
            man_rect.move_ip(-5, 0)
        elif pressed_keys[K_RIGHT] and px<500:
            px += 5
            man_rect.move_ip(5, 0)
        
        ball.move_ip(ball_speed_x, ball_speed_y)

        if ball.colliderect(man_rect):
            #ball_speed_x *= 0
            #ball_speed_y *= 0
            if pressed_keys[K_UP]:
                print("catch")
                ball_speed_x *= 0
                ball_speed_y *= 0
            else:
                print("gameover")
                


        # ボールが画面下に行ったらリセット
        if ball.bottom >= screen_height or ball.bottom <= 30:
            ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, 30, ball_diameter, ball_diameter)
            ball_speed_x = 3 * random.choice((1, -1))
            ball_speed_y = 3 * random.choice((1, -1))

        pygame.draw.ellipse(screen, red, ball)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main()
    
