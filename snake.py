import math
import  random 
import pygame
import tkinter as tk
from tkinter import messagebox
def draw_grid(width, rows,  surface):
    size_between = width // rows
    x = 0
    y = 0
    for _ in range(rows):
        x += size_between
        y += size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

class Cube:
    rows = 20
    width = 500
    def __init__(self, start, dirx=1, diry=0, color=(255, 0, 0)):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i=self.pos[0]
        j=self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre=dis//2
            radius=3
            circlemiddle=(i*dis+centre-radius, j*dis+8)
            circlemiddle2=(i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0),  circlemiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circlemiddle2, radius)

class Snake:
    body = []
    turns = {}
    def  __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_LEFT] and self.dirx != 1:
                        self.dirx = -1
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    elif keys[pygame.K_RIGHT] and self.dirx != -1:
                        self.dirx = 1
                        self.diry = 0
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    elif keys[pygame.K_UP] and self.diry != 1:
                        self.dirx = 0
                        self.diry = -1
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    elif keys[pygame.K_DOWN] and self.diry != -1:
                        self.dirx = 0
                        self.diry = 1
                        self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows-1: c.pos=(c.pos[0], 0)
                elif c.diry == -1 and c.pos[1]<=0: c.pos=(c.pos[0], c.rows-1)
                else: c.move(c.dirx, c.diry)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
    
    def reset(self):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def add_cube(self):
        tail=self.body[-1]
        dx,dy=tail.dirx,tail.diry
        if dx==1 and dy==0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx==-1 and dy==0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx==0 and dy==1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx==0 and dy==-1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))
        self.body[-1].dirx=dx
        self.body[-1].diry=dy

def redraw_win(surface):
    global s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(500, 20, surface)
    pygame.display.update()

def random_snack(rows, item):
    positions=item.body
    while True:
        x=random.randrange(rows)
        y=random.randrange(rows)
        if len(list(filter(lambda z:z.pos==(x,y),positions)))>0:
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    root=tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global s, snack
    win = pygame.display.set_mode((500, 500))
    s = Snake((255, 0, 0), (10, 10))
    rows = 20
    snack=Cube(random_snack(rows,s), color=(0,255,0))
    clock = pygame.time.Clock()
    flag=True
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos==snack.pos:
            s.add_cube()
            snack=Cube(random_snack(rows,s), color=(0,255,0))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print(f"Score: {len(s.body)}")
                message_box("You Lost!", "Play again...")
                s.reset((10,10))
                break
        redraw_win(win)
main()