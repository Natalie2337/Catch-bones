import sys

import pygame
from pygame.locals import *
import random

pygame.init()
canvas_size = [900,800]
screen = pygame.display.set_mode((canvas_size[0], canvas_size[1]))
pygame.display.set_caption('Happy Doge')
bgImg = pygame.image.load('./images/grass.png')
dogeImg = pygame.image.load('./images/doge.png')
boneImg = pygame.image.load('./images/bone.png')
goupenImg = pygame.image.load('./images/goupen.png')
doge_X0 = 430
doge_Y0 = 400

# Sound
pygame.mixer.music.load('./sound/bgm.wav')
pygame.mixer.music.play(-1)

def close_game():
    pygame.quit()
    sys.exit()

fps = 60
fpsClock = pygame.time.Clock()
last_esc_time = pygame.time.get_ticks()
ALLOW_MILISECONDS = 300

class LinearTransform:
    def __init__(self, total_time, updater):
        self.total_time = total_time
        self.updater = updater
        self.now_time = 0
        self.finished = False
    def update(self):
        if self.finished:
            return
        percent = self.now_time/ self.total_time
        if percent > 1:
            self.finished = True
            percent = 1
            return 
        self.now_time += 1/fps
        self.updater(percent)
        
def float2_linear_transform(total_time:float, start_float2:float, end_float2:float, setter):
    directions = [end_float2[0] - start_float2[0], end_float2[1] - start_float2[1]]
    def updater(perc):
        adder = [directions[0] * perc, directions[1] * perc]
        now_value = [start_float2[0] + adder[0], start_float2[1] + adder[1]]
        setter(now_value)
        pass
    return LinearTransform(total_time, updater)
           
           
def pos_linear_transform(total_time, end_pos, obj):
    start_pos = obj.pos
    def setter(new_pos):
        obj.pos = new_pos
    return float2_linear_transform(total_time, start_pos, end_pos, setter)

def distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

class Doge:
    def __init__(self) -> None:
        pass
    def draw(self):
        pos = self.pos
        screen.blit(dogeImg, (pos[0], pos[1]))
        
    def move(self, mov):
        self.pos[0] += mov[0]
        self.pos[1] += mov[1]
        
    def catch_bone(self, bone):
        global Bones
        global score
        if distance(self.pos, bone.pos) < 50:
            Bones.remove(bone)
            score += 1
            print('catch bone')
            print(f"score = {score}")
            
        

dog = Doge()
dog.pos = [doge_X0,doge_Y0]


class Bone:
    def __init__(self):
        pass
    def draw(self):
        pos = self.pos
        screen.blit(boneImg, (pos[0], pos[1]))
        #print('draw bone')
        
    def move(self):
        self.pos[1] += 0.5

#my_bone = Bone()
#my_bone.pos = [300, 200]
#my_bone.draw() 在主循环外面写好像没有用

pressed = set()

ADD_BONE = pygame.USEREVENT + 1
Bones = []    

pygame.time.set_timer(ADD_BONE, 1000) # timer 

# Score
score = 0
font = pygame.font.Font(None, 36)
def show_score():
    score_text = font.render(f"Bone: {score}", True, (255, 0, 127)) # 最后这个参数是字体颜色
    screen.blit(score_text, (750, 70))
    

while True:
    screen.blit(bgImg, (0,0))   
    screen.blit(goupenImg, (750, 100))
    show_score()
    
    dog.draw()
    #my_bone.draw()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            close_game()
        if event.type == KEYDOWN and event.dict['scancode'] == 41:
            now = pygame.time.get_ticks()
            dif = now - last_esc_time
            if dif <= ALLOW_MILISECONDS:
                close_game()
            else:
                last_esc_time = now
        if event.type == ADD_BONE:
            print('add bone')
            bone = Bone()
            rand_x = random.randint(100, 700)
            bone.pos = [rand_x, 0]
            print(bone.pos)
            #bone.draw()
            Bones.append(bone)
    
            
        if event.type == KEYDOWN:
            if event.dict['key'] == 97:
                #A
                #print(event.dict['scancode']) 
                #print(event.dict['key'])  
                pressed.add(1)  
            elif event.dict['key'] == 100: 
                #D
                pressed.add(2)
            elif event.dict['key'] == 115:
                #S
                pressed.add(3)
            elif event.dict['key'] == 119:
                #W
                pressed.add(4)
        
        if event.type == KEYUP:
            if event.dict['key'] == 97:
                pressed.discard(1)    
            elif event.dict['key'] == 100:
                pressed.discard(2)
            elif event.dict['key'] == 115:
                pressed.discard(3)
            elif event.dict['key'] == 119:
                pressed.discard(4)
            
    movement = [0,0]    
    if 1 in pressed:
        movement[0] = -0.3
    if 2 in pressed:
        movement[0] = 0.3
    if 3 in pressed:
        movement[1] = 0.3
    if 4 in pressed:
        movement[1] = -0.3
        
    #print(dog.pos)
    
    # boundaries
    if dog.pos[0] > 845:
        dog.pos[0] = 830
    if dog.pos[0] < 0:
        dog.pos[0] = 15
    if dog.pos[1] > 400:
        dog.pos[1] = 400  
    if dog.pos[1] < 0:
        dog.pos[1] = 15

    
    for bone in Bones:
        bone.draw()
        bone.move()
        dog.catch_bone(bone)
        if bone.pos[1] > 800:
            Bones.remove(bone)
            
    dog.move(movement)
      
    pygame.display.flip()

