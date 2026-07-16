import random
import math
import time
from collections import Counter
import json
import os
import sys
#region INIT
WIDTH = 0
HEIGHT = 0
GRIDWIDTH = 0
GRIDHEIGHT = 0
CELLSIZE = 0
particleSize = 0

def init(width, height, gridwidth, gridheight, cellsize):
    global WIDTH, HEIGHT, GRIDWIDTH, GRIDHEIGHT, CELLSIZE, particleSize

    WIDTH = width
    HEIGHT = height
    GRIDWIDTH = gridwidth
    GRIDHEIGHT = gridheight
    CELLSIZE = cellsize
    particleSize = CELLSIZE

def returnCoordinates(x, y):
    x = int(x // CELLSIZE)
    y = int(y // CELLSIZE)

    return (
        min(GRIDHEIGHT, max(0, y)),
        min(GRIDWIDTH, max(0, x))
    )

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

with open(resource_path("data.json"), "r", encoding="utf-8") as f:
    gameData = f.read()


#endregion
#region Reaction class
class Reactions():
    def __init__(self):
        self.data = json.loads(gameData)
        self.rules = {
            tuple(map(int, k.split(","))): v
            for k, v in self.data["reactions"].items()
        }

    def count(self, cell:list):
        return dict(Counter(cell))

    def react(self, cell):
        counts = self.count(cell)
        results = []
        for rule, effect in self.rules.items():
            if all(counts.get(x, 0) > 0 for x in rule):
                results.append(effect)

        return results
#endregion
reactor = Reactions()

#region Game class
class Game():
    def __init__(self,gravity,tick,airDens):
        self.gravity = gravity
        self.tick = tick
        self.veri = json.loads(gameData)
        self.airDensity = airDens
    
    def reaction(self,cell):
        particles = [int(particle.id) for particle in cell]
        result = ["0",cell]
        if reactor.react(particles):
            result = [reactor.react(particles),cell]
        return result


    
    def spawner(self,id,x,y,pygame):
        tip = self.veri["particles"][str(id)]["type"]
        particle = self.veri["particles"][str(id)]
        match tip :
            
            case "nuclear":
                part = Nuclear(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"])
                return part

            case "powder":
                part = Powder(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"])
                return part

            case "solid":
                part = Solid(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"])
                return part

            case "liquid":
                part = Liquid(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"])
                return part

            case "gas":
                part = Gas(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"])
                return part

            case "energy":
                part = Energy(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),particle["color"],particle["lifetime"])
                return part


            case _:
                pass





    def particleData(self,id):
        return self.veri["particles"][str(id)]
#endregion

#region Main Particle class
class Particle:

    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,x_velocity=0,y_velocity=0,sh=1,lifeTime = -1):
        self.name = name
        self.pygame = pygame
        self.temp = max(-273.15 , min(temp,9500))
        self.sh = sh #Oz Isı
        self.mass = mass
        self.color =  tuple(random.choice(color))
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.id = particleId
        self.lifeTime = lifeTime 
    #* Düzeldi    
    def draw(self,win,grid):
        self.pygame.draw.rect(win, self.color, (self.x, self.y, particleSize, particleSize))
        value = returnCoordinates(self.x,self.y)
        theGrid = grid[value[0]][value[1]]
        if self not in theGrid:theGrid.append(self)

    #*Düzeldi
    def gravity(self,win,gravity,dt,grid,theGame):
        if self.y <= HEIGHT:
            value = returnCoordinates(self.x,self.y+3)
            downCell = grid[value[0]][value[1]]
            if downCell and any(item.type in ("solid", "powder") or item.type == self.type for item in downCell):
                self.y_velocity = 0
                return
            
            gravity = int(round(gravity * dt * 15 / particleSize) * particleSize) 
            self.y_velocity += gravity
            if self.y_velocity >= particleSize:
                self.y_velocity = particleSize
            self.y += self.y_velocity
            
        



    def checkLifeTime(self):
        if  self.lifeTime >= 0:    
            if self.time >= self.lifeTime:
                return True
            self.time += 1
        else:pass



    def checkCollision(self,grid,x=None,y=None):
        x = x or self.x
        y = y or self.y
        if 0 < x < WIDTH and 0 < y < HEIGHT:
            value = returnCoordinates(x,y)
            cell = grid[value[0]][value[1]]
            if len(cell) >= 1 :
                return [True,(x,y),cell]
            else:
                return [False,0]
        return [False,0]


    def move(self,win,dt,grid):pass

    def drawGlow(self,win):pass
#endregion

#region Nuclear class
class Nuclear(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,x_velocity=250,y_velocity=250,lifeTime = 500):
        self.name = name
        self.pygame = pygame
        self.temp = temp
        self.mass = mass
        self.color = color
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.degree = math.radians(random.randint(1,360))
        self.id = particleId
        self.lifeTime = lifeTime
        self.time = 0
        self.type = "nuclear"

        super().__init__(name,particleId,pygame,x,y,temp,mass,color,x_velocity,y_velocity,lifeTime=self.lifeTime)


    def gravity(self,win,gravity,dt,grid,theGame):pass

    #! Düzelt kotu oldu
    def move(self,win,dt,grid):
        if 0 < self.x < WIDTH and 0 < self.y < HEIGHT:
            value = returnCoordinates(self.x,self.y)
            cell = grid[value[0]][value[1]]
            self.x += math.cos(self.degree) * self.x_velocity * dt * 0.5
            self.y += math.sin(self.degree) * self.y_velocity * dt * 0.5
            self.x , self.y = int(round(self.x/particleSize)*particleSize) , int(round(self.y/particleSize)*particleSize)
            if self not in cell:
                cell.append(self)
                return cell

    def drawGlow(self,win):
        glow = self.pygame.Surface((9,9))
        glow.set_alpha(64)
        glow.fill(self.color)

        win.blit(glow,(self.x-particleSize,self.y-particleSize))
#endregion

#region Powder class
class Powder(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color):
        self.name = name
        self.particleID = particleId
        self.pygame = pygame
        self.x = x 
        self.y = y
        self.temp = temp
        self.mass = mass
        self.color = color
        self.type = "powder"

        super().__init__(name,particleId,pygame,x,y,temp,mass,color)


    #* Düzeldi
    def move(self,win,dt,grid):
        downCell = []
        moveTo = random.randint(0, 1) * 2 - 1
        if 0 < self.x < WIDTH and 0 < self.y < HEIGHT:
            value = returnCoordinates(self.x,self.y+3)
            downCell = grid[value[0]][value[1]]
            verticalValue = returnCoordinates(self.x+moveTo*3,self.y)
            horizontalValue = returnCoordinates(self.x+moveTo*3,self.y+3)
            if len(downCell) > 0:
                gotoCell , block = [grid[horizontalValue[0]][horizontalValue[1]],grid[verticalValue[0]][verticalValue[1]]]
                if (len(gotoCell) > 0 or len(block) > 0 ) and (any(item.type in ("solid", "powder") or item.type == self.type for item in gotoCell) or any(item.type in ("solid", "powder") or item.type == self.type for item in block)):moveTo *= -1

                gotoCell , block = [grid[horizontalValue[0]][horizontalValue[1]],grid[verticalValue[0]][verticalValue[1]]]
                if (len(gotoCell) > 0 or len(block) > 0 ) and (any(item.type in ("solid", "powder") or item.type == self.type for item in gotoCell) or any(item.type in ("solid", "powder") or item.type == self.type for item in block)):moveTo *= 0
            
            else:moveTo *= 0

            self.x += int(moveTo*particleSize)
            gotoX , gotoY = self.x//particleSize , self.y //particleSize 
            value = returnCoordinates(gotoX,gotoY)
            cell = grid[value[0]][value[1]]
            
            if self not in cell:
                cell.append(self)
                return cell
#endregion

#region Solid class
class Solid(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color):
        self.name = name
        self.particleID = particleId
        self.pygame = pygame
        self.x = x 
        self.y = y
        self.temp = temp
        self.mass = mass
        self.color = color
        self.type = "solid"

        super().__init__(name,particleId,pygame,x,y,temp,mass,color)


    def gravity(self,win,gravity,dt,grid,theGame):pass

    def move(self,win,dt,grid):
        value = returnCoordinates(self.x,self.y)
        theGrid = grid[value[0]][value[1]]
        if not self in theGrid:
            theGrid.append(self)            
#endregion

#region Liquid class
class Liquid(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color):
        self.name = name
        self.particleID = particleId
        self.pygame = pygame
        self.x = x 
        self.y = y
        self.temp = temp
        self.mass = mass
        self.color = color
        self.type = "liquid"

        super().__init__(name,particleId,pygame,x,y,temp,mass,color)


    #* Düzeldi
    def move(self,win,dt,grid):
        downCell = []
        moveTo = random.randint(0, 1) * 2 - 1
        value = returnCoordinates(self.x,self.y+3)
        downCell = grid[value[0]][value[1]]
        if len(downCell) > 0:
            value = returnCoordinates(self.x+moveTo*3,self.y)
            gotoCell = grid[value[0]][value[1]]
            if len(gotoCell) > 0:
                moveTo *= -1
            value = returnCoordinates(self.x+moveTo*3,self.y)
            gotoCell = grid[value[0]][value[1]]
            if len(gotoCell) > 0:
                moveTo *= 0
        else:moveTo *= 0

        self.x += int(moveTo*particleSize)
        value = returnCoordinates(self.x,self.y)
        cell = grid[value[0]][value[1]]
        if len(cell) >1:
            if any(item.type == "powder" for item in cell):
                roadFound = False
                road = 0
                while not roadFound:
                    value = value = returnCoordinates(self.x,self.y-road*3)
                    if len(grid[value[0]][value[1]]) ==0:
                        roadFound = True
                        road*=particleSize
                    else:
                        road+=1
                self.y -= road
                value = returnCoordinates(self.x,self.y)
                grid[value[0]][value[1]].append(self)
            cell = grid[value[0]][value[1]]
            
        if self not in cell:
            cell.append(self)
            return cell
#endregion

#region Gas class
class Gas(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,density=1.100):
        self.name = name
        self.particleID = particleId
        self.pygame = pygame
        self.x = x 
        self.y = y
        self.temp = temp
        self.mass = mass
        self.color = color
        self.type = "gas"
        self.density = density


        super().__init__(name,particleId,pygame,x,y,temp,mass,color)

    def gravity(self,win,gravity,dt,grid,theGame):
        direction  = -1*((self.y_velocity > 0) - (self.y_velocity < 0))
        value = -((theGame.airDensity - self.density) * dt)
        value = 0 if value == 0 else int(math.copysign(max(1, round(abs(value) / particleSize)), value) * particleSize)
        self.y_velocity +=  value

        if self.y_velocity != value:
            self.y_velocity = value
        gridValue = returnCoordinates(self.x,self.y+value)
        if len(grid[gridValue[0]][gridValue[1]]) > 0:
            self.y_velocity = 0
            self.x += int(direction * particleSize)
            return

        self.y += self.y_velocity
        gridValue = returnCoordinates(self.x+direction,self.y)
        grid[gridValue[0]][gridValue[1]]


    def move(self,win,dt,grid):
        moveTo = random.randint(0,1) * 2 - 1
        value = returnCoordinates(self.x+moveTo*3,self.y)
        gotoCell = grid[value[0]][value[1]]
        if len(gotoCell) > 0:
            moveTo *= -1
        gotoCell = grid[value[0]][value[1]]
        if len(gotoCell) > 0:
            moveTo *= 0

        moveTo = int(moveTo*particleSize)
        self.x += moveTo
#endregion

#region Energy class
class Energy(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,lifeTime:str):
        self.name = name
        self.particleID = particleId
        self.pygame = pygame
        self.x = x 
        self.y = y
        self.temp = temp
        self.mass = mass
        self.color = color
        self.type = "energy"
        self.time = 0
        lifeTime = lifeTime.split("/*/")
        self.lifeTime = random.randint(int(lifeTime[0]),int(lifeTime[1]))

        super().__init__(name,particleId,pygame,x,y,temp,mass,color,lifeTime=self.lifeTime)

    def gravity(self,win,gravity,dt,grid,theGame):...

    def drawGlow(self,win):
        glow = self.pygame.Surface((9,9))
        glow.set_alpha(64)
        glow.fill(self.color)

        win.blit(glow,(self.x-particleSize,self.y-particleSize))

    def move(self, win, dt, grid):
        value = returnCoordinates(self.x, self.y)

        while True:
            moveToX = random.randint(-1, 1)
            moveToY = -1
            if moveToX != 0 or moveToY != 0:
                break

        newY = min(max(value[0] + moveToY, 0), GRIDHEIGHT)
        newX = min(max(value[1] + moveToX, 0), GRIDWIDTH)

        targetCell = grid[newY][newX]

        if len(targetCell) > 0:
            return

        self.x += moveToX * CELLSIZE
        self.y += moveToY * CELLSIZE

        value = returnCoordinates(self.x, self.y)
        cell = grid[value[0]][value[1]]

        if self not in cell:
            cell.append(self)
            return cell
#endregion
