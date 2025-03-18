import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

ALLOW_MILISECONDS = 300

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

last_esc_time = pygame.time.get_ticks()

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

class Ball:
    def __init__(self) -> None:
        pass
    def draw(self):
        size = self.size
        color = self.color
        pos = self.pos
        pygame.draw.ellipse(screen, color, (pos[0], pos[1], size, size)) 
        
    def move(self, mov):
        self.pos[0] += mov[0]
        self.pos[1] += mov[1]
        

b = Ball()
b.size = 80
b.color = pygame.Color(100,200,100)
b.pos = [100,120]

def close_game():
    pygame.quit()
    sys.exit()

t1 = pos_linear_transform(2, [200, 200], b)

xy_axis = [0, 0]
XY_AXIS_DEFAULT = [0, 0]
pressed = set()

while True:
    screen.fill((0, 0, 0))
    
    xy_axis[0], xy_axis[1] = XY_AXIS_DEFAULT[0], XY_AXIS_DEFAULT[1]

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
        #A
        if event.type == KEYDOWN and event.dict['key'] == 97:
            #print(event.dict['scancode']) 
            #print(event.dict['key'])  
            pressed.add(1)  
        #D
        if event.type == KEYDOWN and event.dict['key'] == 100:   
            pressed.add(2)
        #S
        if event.type == KEYDOWN and event.dict['key'] == 115:  
            pressed.add(3)
        #W
        if event.type == KEYDOWN and event.dict['key'] == 119:  
            pressed.add(4)
        
        if event.type == KEYUP and event.dict['key'] == 97:
            pressed.discard(1)    
        if event.type == KEYUP and event.dict['key'] == 100:
            pressed.discard(2)
        if event.type == KEYUP and event.dict['key'] == 115:
            pressed.discard(3)
        if event.type == KEYUP and event.dict['key'] == 119:
            pressed.discard(4)
            
    movement = [0,0]    
    if 1 in pressed:
        movement[0] = -1
    if 2 in pressed:
        movement[0] = 1
    if 3 in pressed:
        movement[1] = 1
    if 4 in pressed:
        movement[1] = -1
    #t1.update()
    b.move(movement)
    b.draw()
    pygame.display.flip()
    fpsClock.tick(fps)
