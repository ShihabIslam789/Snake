import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

width = 500
height = 500

cols = 25
rows = 20


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        # BY multiyping row and column value by our cubes width and height of each cube we can
        # determine where to draw
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos) #head will be front of snake
        self.body.append(self.head) #add head which is a cube
        #below are directions of snake movement
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #checks if user presses the 'x' button
                pygame.quit()
            keys = pygame.key.get_pressed() # see which keys are pressed

            for key in keys: #loop through all keys
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body): #loop through every cube in body
            p = c.pos[:]    # This stores cubes position on the grid
            if p in self.turns: #If cubes current position is one where we turned
                turn = self.turns[p] #Get the direction we should turn
                c.move(turn[0], turn[1]) #move our cube in that direction
                if i == len(self.body)-1:#If last cube, remove from dictionary
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny) #otherwise move in headed direction
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # We need to know which side of the snake to add the cube to.
        # SO we check what direction we are moving in to determine if we need
        # to add the cube to the left,right, above or below
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows #Distance between Lines

    x = 0 # keep track of x
    y = 0 #keep track of y
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    


def randomSnack(rows, item):
    positions = item.body #Get all positions of our cubes

    while True: #keep generating random positions until we get a valid one
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # This checks if the position we generated is occupied by the snake
               continue
        else:
               break

    return (x,y)

def message_box(subject, content):
    #using tkinder for out of game msgs
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global s, snack, win
    win = pygame.display.set_mode((width,height))
    s = snake((255,0,0), (10,10))
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(0,255,0))
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(s.body))
            s.reset((10, 10))

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(0,255,0))
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #check if body overlaps from y position
                print("Score:", len(s.body))
                message_box("You Lost!","Try Again!")
                s.reset((10,10))
                break
                    
        redrawWindow()

main()