import pygame as pg
from pygame.locals import *
import time
import random

SIZE = 25

class Apple:
    def __init__(self,parent_screen) :
        self.parent_screen = parent_screen
        self.image = pg.image.load("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/apple.jpg").convert()
        self.x = 125
        self.y = 125

    def draw(self):
        
        self.parent_screen.blit(self.image, (self.x, self.y))
        pg.display.flip()
        

    def move(self):
        self.x = random.randrange(25,1000,50)
        self.y = random.randrange(25,800,50)
        
     


class Snake:
    def __init__(self, parent_screen, length) :
        
        self.parent_screen = parent_screen
        self.block = pg.image.load("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/snake.jpg").convert()
        
        self.direction = 'right'

        self.length = length
        self.block_x=[25]*length
        self.block_y=[25]*length


    
    def move_up(self):
        self.direction='up'
    def move_down(self):
        self.direction='down'
    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]
        if self.direction=='up':
            self.block_y[0]-=25
        if self.direction=='down':
            self.block_y[0]+=25
        if self.direction=='right':
            self.block_x[0]+=25
        if self.direction=='left':
            self.block_x[0]-=25

        self.draw()

    def draw(self):

        self.parent_screen.fill((110,110,5))
        for i in range (self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))
        pg.display.flip()

    def increase_length(self):
        self.length+=1
        self.block_x.append(-1)
        self.block_y.append(-1)


class Game:
    def __init__(self) :
        pg.init()

        pg.mixer.init()

        self.MAX_SCORE=0

        self.play_background_music()

        self.surface = pg.display.set_mode((1000,800))

        self.snake = Snake(self.surface,1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    
    
    def reset(self):

        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    
    def display_score(self):
        font = pg.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length-1}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def play_background_music(self):
        pg.mixer.music.load("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/031985_a-soothing-songmp3-75457.mp3")
        pg.mixer.music.play(loops=999)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pg.display.flip()

        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0],self.apple.x, self.apple.y):
            
            self.snake.increase_length()
            sound = pg.mixer.Sound("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/swallow.mp3")
            pg.mixer.Sound.play(sound)
            self.apple.move()

        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                sound = pg.mixer.Sound("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/crash-6711.mp3")
                pg.mixer.Sound.play(sound)
                raise "Game Over"
            
        if self.snake.block_x[0]<0 or self.snake.block_x[0]>=1000 or self.snake.block_y[0]<0 or self.snake.block_y[0]>800:
            sound = pg.mixer.Sound("C:/Users/PRATAP/Documents/Codes/Python/SNAKE_GAME/crash-6711.mp3")
            pg.mixer.Sound.play(sound)
            raise "Game Over"
            
    def show_game_over(self):
        pg.mixer.music.pause()
        self.MAX_SCORE = max(self.MAX_SCORE, self.snake.length-1)
        self.surface.fill((110,110,5))
        font = pg.font.SysFont('arial',30)
        line0 = font.render("GAME OVER", True, (255,255,255))
        self.surface.blit(line0, (200,250))
        line1 = font.render(f"SCORE: {self.snake.length-1} | HIGH SCORE : {max( self.MAX_SCORE, self.snake.length-1)}" , True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To Play Again Press ENTER , To Exit Press ESCAPE", True, (255,255,255))
        self.surface.blit(line2, (200,350))
        
        pg.display.flip()


    def run (self):
        running = True
        pause = False
    
        while running:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN or event.key== K_KP_ENTER:
                        pg.mixer.music.unpause()
                        pause = False

                    if not pause:
                    

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            
            time.sleep(0.1)
            
    
if __name__ == "__main__":
    game = Game()
    game.run()

    
 
