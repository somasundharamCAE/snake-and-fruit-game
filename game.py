#snake_and_Fruit_game
import pygame
from pygame.locals import *
import time
import random

class Snake:
    def __init__(self,window,length):
        self.screen=window
        self.length=length
        self.snake_head=pygame.image.load("S:/DOCS/snake_game/snake_head.png").convert()
        self.snake_body=pygame.image.load("S:/DOCS/snake_game/snake_body.png").convert()
        self.snake_head_x=[300]*self.length
        self.snake_head_y=[400]*self.length
        self.direction='right'
    
    def draw_snake(self):
        self.screen.blit(self.snake_head,(self.snake_head_x[0],self.snake_head_y[0]))
        for i in range(1,self.length):
            self.screen.blit(self.snake_body,(self.snake_head_x[i],self.snake_head_y[i]))
            pygame.display.update()

    def increase_length(self):
        self.snake_head_x.append(1)
        self.snake_head_y.append(1)
        self.length+=1

        
    def move_up(self):
        self.direction='up'
        
    def move_down(self):
        self.direction='down'
        
    def move_left(self):
        self.direction='left'
        
    def move_right(self):
        self.direction='right'

    def snake_hits_wall(self):
        if self.snake_head_x[0]>=700:
            self.snake_head_x[0]=0
        if self.snake_head_y[0]>=750:
            self.snake_head_y[0]=0
        if self.snake_head_x[0]<0:
            self.snake_head_x[0]=700
        if self.snake_head_y[0]<0:
            self.snake_head_y[0]=750
        
    def motion(self):
        for i in range(self.length-1,0,-1):
            self.snake_head_x[i]=self.snake_head_x[i-1]
            self.snake_head_y[i]=self.snake_head_y[i-1]
        if self.direction=='up':
            self.snake_head_y[0]-=25
        if self.direction=='down':
            self.snake_head_y[0]+=25
        if self.direction=='left':
            self.snake_head_x[0]-=25
        if self.direction=='right':
            self.snake_head_x[0]+=25
        self.snake_hits_wall()
        self.draw_snake()

class Fruit:
    def __init__(self,window):
        self.screen=window
        self.fruit=pygame.image.load("S:/DOCS/snake_game/fruit.png").convert()
        self.fruit_x,self.fruit_y=random.randint(1,27)*25,random.randint(1,29)*25
    
    def draw_fruit(self):
        self.screen.blit(self.fruit,(self.fruit_x,self.fruit_y))
        pygame.display.update()

    def move_fruit(self):
        self.fruit_x=random.randint(1,26)*25
        self.fruit_y=random.randint(1,27)*25


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("snake and fruit game")
        self.window=pygame.display.set_mode((700,750))
        self.snake=Snake(self.window,2)
        self.snake.draw_snake()
        self.fruit=Fruit(self.window)
        self.fruit.draw_fruit()
        self.speed=0.38
        self.bg_music()

    def collision(self,x1,y1,x2,y2):
        if x1<(x2+25) and y1<(y2+25):
            if x1>=x2 and y1>=y2:
                return 1
        else:
            return 0
        
    def sound_play(self,name):
        sound=pygame.mixer.Sound(f"S:/DOCS/snake_game/{name}.mp3")
        pygame.mixer.Sound.play(sound)

    def bg_music(self):
        pygame.mixer.music.load("S:/DOCS/snake_game/bg_music.mp3")
        pygame.mixer.music.play(1,0)
        
    def display_score(self):
        font1=pygame.font.SysFont('calibri',26)
        score=font1.render("SCORE: {}".format(self.snake.length-2),True,(61, 51, 56))
        self.window.blit(score,(570,7))
        pygame.display.update()

    def game_over(self):
        self.window.fill((252,127,3))
        font2=pygame.font.SysFont('arial',40)
        line_1=font2.render("GAME OVER",True,(61, 51, 56))
        self.window.blit(line_1,(250,300))
        font3=pygame.font.SysFont('calibri',24)
        line_2=font3.render("To Continue, Press ENTER or To Exit, Press ESC",True,(61, 51, 56))
        self.window.blit(line_2,(140,360))
        pygame.display.update()

    def reset(self):
        self.snake=Snake(self.window,2)
        self.snake.draw_snake()
        self.fruit=Fruit(self.window)
        self.fruit.draw_fruit()
        
    def play(self):
        self.window.fill((252,127,3))
        self.snake.motion()
        self.fruit.draw_fruit()
        self.display_score()

        #snake colliding with fruit
        if self.collision(self.snake.snake_head_x[0],self.snake.snake_head_y[0],self.fruit.fruit_x,self.fruit.fruit_y):
            self.fruit.move_fruit()
            self.sound_play('ding')
            self.snake.increase_length()
            self.speed-=0.005
        
        #snake colliding itself
        for i in range(1,self.snake.length):
            if self.collision(self.snake.snake_head_x[0],self.snake.snake_head_y[0],self.snake.snake_head_x[i],self.snake.snake_head_y[i]):
                self.pause=False
                self.sound_play('crash')
                pygame.mixer.music.pause()
    
    def run(self):
        running=True
        self.pause=True
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if not self.pause:
                        if event.key==K_ESCAPE:
                            running=False
                        if event.key==K_RETURN:
                            self.pause=True
                            self.reset()
                            pygame.mixer.music.unpause()
                    if event.key==K_ESCAPE:
                            running=False
                    if event.key==K_UP:
                        self.snake.move_up()
                    if event.key==K_DOWN:
                        self.snake.move_down()
                    if event.key==K_RIGHT:
                        self.snake.move_right()
                    if event.key==K_LEFT:
                        self.snake.move_left()
                elif event.type==QUIT:
                    running=False

            if self.pause:
                self.play()
            else:
                self.game_over()
            time.sleep(self.speed)

if __name__=='__main__':
    game=Game()
    game.run()