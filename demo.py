import pygame
from pygame.locals import *
import random
import sys
import time
import backgroundPlay

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

def sound():
    pygame.mixer.init() #初期化

    pygame.mixer.music.load("image\\unmei.mp3") #読み込み

    pygame.mixer.music.play(4) #再生

    time.sleep(3)

    pygame.mixer.music.stop() #終了

def fin():
    font1 = pygame.font.SysFont("hg正楷書体pro", 50)
    font2 = pygame.font.SysFont("hg正楷書体pro", 20)
    button = pygame.Rect(140, 200, 320, 50)
    text4 = font1.render("終了", True, (0,0,0))
    button_retry=pygame.Rect(200,260,200,50)
    text5=font2.render("もう一回挑戦する",True,(0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), button)
    pygame.draw.rect(screen, (255, 0, 0), button_retry)
    screen.blit(text4, (250,202))
    screen.blit(text5, (220,262))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    print("fin button was pressed")
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def main():
    font1 = pygame.font.SysFont("hg正楷書体pro", 50)
    font2 = pygame.font.SysFont("hg正楷書体pro", 30)

    leveltext1 = font2.render("レベル1", True, (0,0,0))
    leveltext2 = font2.render("レベル2", True, (0,0,0))
    leveltext3 = font2.render("レベル3", True, (0,0,0))
    leveltext4 = font2.render("レベル4", True, (0,0,0))
    leveltext5 = font2.render("レベル5", True, (0,0,0))

    button1 = pygame.Rect(50, 50, 150, 30)
    button2 = pygame.Rect(50, 100, 150, 30)
    button3 = pygame.Rect(50, 150, 150, 30)
    button4 = pygame.Rect(50, 200, 150, 30)
    button5 = pygame.Rect(50, 250, 150, 30)


    text1 = font1.render("ゲームオーバー", True, (255,0,255))
    text2 = font1.render("キャッチ", True, (255,0,255))
    text3 = font1.render("ゲームクリア", True, (255,0,255))
    
    px=250
    py=300

    ex=250
    ey=0
    
    man = pygame.image.load("image\\syougakusei.png")
    man = pygame.transform.scale(man,(100,100))
    man_rect = pygame.Rect(250, 300, 100, 100)

    oct = pygame.image.load("image\\utyuujin.png")
    oct = pygame.transform.scale(oct,(100,100))
    oct_rect = pygame.Rect(250, 0, 100, 100)

    ball_diameter = 30
    ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, 30, ball_diameter, ball_diameter)
    #ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, screen_height // 2 - ball_diameter // 2, ball_diameter, ball_diameter)
    ball_speed_x = 3 * random.choice((1, -1))
    ball_speed_y = 3 * random.choice((1, 0.5))

    attack=0

    levelchoice = 1

    buff=1
    

    while True:
         
        screen.fill(white)

        while levelchoice == 1:
            for event in pygame.event.get():
                pygame.draw.rect(screen, (255, 0, 0), button1)
                pygame.draw.rect(screen, (255, 0, 0), button2)
                pygame.draw.rect(screen, (255, 0, 0), button3)
                pygame.draw.rect(screen, (255, 0, 0), button4)
                pygame.draw.rect(screen, (255, 0, 0), button5)

                screen.blit(leveltext1,(55,55))
                screen.blit(leveltext2,(55,105))
                screen.blit(leveltext3,(55,155))
                screen.blit(leveltext4,(55,205))
                screen.blit(leveltext5,(55,255))

                if event.type == QUIT:  # 終了イベント
                    pygame.quit()  #pygameのウィンドウを閉じる
                    sys.exit() #システム終了
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1.collidepoint(event.pos):
                        print("level1")
                        levelchoice=0
                        buff=1
                    if button2.collidepoint(event.pos):
                        print("level2")
                        levelchoice=0
                        buff=2
                    if button3.collidepoint(event.pos):
                        print("level3")
                        levelchoice=0
                        buff=3
                    if button4.collidepoint(event.pos):
                        print("level4")
                        levelchoice=0
                        buff=4
                    if button5.collidepoint(event.pos):
                        print("level5")
                        levelchoice=0
                        buff=5
                    if 1<=buff and buff<=5:
                        backgroundPlay.SoundPlayer.play("bgm.mp3")
            ball_speed_x *= buff
            ball_speed_y *= buff
            pygame.display.update()

        screen.blit(man,(px,py))
        screen.blit(oct,(ex,ey))

        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys =pygame.key.get_pressed()
        
        ball.move_ip(ball_speed_x, ball_speed_y)

        if ball.colliderect(man_rect):
            ball_speed_x *= 0
            ball_speed_y *= 0
            if pressed_keys[K_UP]:
                screen.blit(text2, (200,150))
                if pressed_keys[K_LEFT] and ball.left>0 and px>0:
                    ball.move_ip(-5, 0)                    
                    px -= 5
                    man_rect.move_ip(-5, 0)
                elif pressed_keys[K_RIGHT] and ball.right<600 and px<500:
                    ball.move_ip(5, 0)
                    px += 5
                    man_rect.move_ip(5, 0)
                elif pressed_keys[K_DOWN]:
                    ball_speed_x = 3 * random.choice((0.4*buff, -0.4*buff))
                    ball_speed_y = 3 * random.choice((0.5*buff, -1*buff))
                    attack=1
            else:
                screen.blit(text1, (120,150))
                pressed_keys =0
                #print("gameover")
                backgroundPlay.SoundPlayer.play("image/unmei.mp3",stop=True)
                fin()
        else:
            if pressed_keys[K_UP]:
                print("キャッチ")
                print("待機")
            else:
                if pressed_keys[K_LEFT] and px>0:
                    px -= 5
                    man_rect.move_ip(-5, 0)
                elif pressed_keys[K_RIGHT] and px<500:
                    px += 5
                    man_rect.move_ip(5, 0)
        
        if ball.colliderect(oct_rect):
            #print("game")
            if attack==1:
                #print("gameclear")
                ball_speed_x *= 0
                ball_speed_y *= 0
                screen.blit(text3, (160,150))
                fin()
            
                
        # ボールが画面の端に当たったら反射
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed_x *= -1

        # ボールが画面上下に行ったらリセット
        if ball.bottom >= screen_height or ball.bottom <= 30:
            attack=0
            ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, 30, ball_diameter, ball_diameter)
            ball_speed_x = 3 * random.choice((1*buff, -1*buff))
            ball_speed_y = 3 * random.choice((1*buff, 0.5*buff))
        if ball.top <= 0:
            attack=0
            ball_speed_y *= -1

        pygame.draw.ellipse(screen, red, ball)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main()
    
