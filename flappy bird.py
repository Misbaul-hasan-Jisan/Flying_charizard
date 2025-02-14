import pygame
from pygame.locals import *
import random
from pygame import mixer
pygame.init()
#background sound
#mixer.music.load('audio/bgmusic2.wav')
#mixer.music.play(-1)
clock=pygame.time.Clock()
fps=60
pygame.display.set_caption("flying charizard")
SCREEN_WIDTH=900
SCREEN_HIGHT=700
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
ground_scroll=1
scroll_speed=4
flying=False
game_over=False
pipe_gap = 350
pipe_frequency= 1800
last_pipe=pygame.time.get_ticks()-pipe_frequency
score=0
pass_pipe= False
font = pygame.font.SysFont('Bauhaus 93', 60)
white =(255,255,255)
#load image
bg=pygame.image.load('img/bg.png')
ground=pygame.image.load('img/ground.png')
restart_button=pygame.image.load('img/restart.png')
def draw_text(text,font,text_col,x,y):
    img= font.render(text,True,text_col)
    screen.blit(img,(x,y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(SCREEN_HIGHT / 2)
	score = 0
	return score



class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,9):
            img=pygame.image.load(f'img/chari{num}.png')
            self.images.append(img)

        self.image= self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False

    def update(self):
        if flying==True:
              self.vel+=0.5
              if self.vel>6:
                self.vel=6
              if self.rect.bottom<600:
                 self.rect.y+=int(self.vel)
       
        #jump
        if game_over==False:
               if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                  self.clicked=True
                  self.vel=-10	
               if pygame.mouse.get_pressed()[0] == 0:
                 self.clicked=False
                #handle animation
                 self.counter += 1
                 flap_cooldown = 5
                 if self.counter > flap_cooldown:
                  self.counter = 0
                  self.index += 1
                  if self.index >= len(self.images):
                   self.index=0
                 self.image=self.images[self.index]                    
                 #rotate the bird      
                 self.image=pygame.transform.rotate(self.images[self.index],self.vel*-1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('img/pipe2.png')
        self.rect=self.image.get_rect()
        if position==1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y- int(pipe_gap / 2)]
        if position==-1:
            self.rect.topleft=[x,y+ int(pipe_gap / 2)]
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image= image
        self.rect=self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action =False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action       


bird_group=pygame.sprite.Group()
flappy=Bird(100,int( SCREEN_HIGHT / 2))
bird_group.add(flappy)
pipe_group=pygame.sprite.Group()
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HIGHT // 2 - 100, restart_button)     
# Game loop
run=True
while run==True:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    screen.blit(ground,(ground_scroll,600))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    #check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False
    draw_text(str(score), font, white, int(SCREEN_WIDTH / 2), 20)
    

   
                
         
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over=True
        mixer.music.load('audio/deathsound.wav')
        mixer.music.play()

    if flappy.rect.bottom > 600:
        game_over=True
        flying=False
        
	
    if game_over==False and flying==True:
        time_now=pygame.time.get_ticks()
        if time_now - last_pipe> pipe_frequency:
            pipe_height=random.randint(-100,100)
            btm_pipe=Pipe(SCREEN_WIDTH,int( SCREEN_HIGHT / 2)+pipe_height,-1)
            top_pipe=Pipe(SCREEN_WIDTH,int( SCREEN_HIGHT / 2)+pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now       
    ground_scroll-=scroll_speed
    if abs(ground_scroll)>35:
        ground_scroll=0
    pipe_group.update()

    if game_over==True:
        mixer.music.load('audio/bgmusic2.wav')
        mixer.music.play(-1)
        scroll_speed=0
        if button.draw() == True:
            game_over = False
            score=reset_game()
            scroll_speed=4  
   
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True


    pygame.display.update()
pygame.quit()