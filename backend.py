import random
import math
import time
from collections import Counter
import json
import os
import sys

WIDTH = 900
HEIGHT = 600

GRIDWIDTH = 300
GRIDHEIGHT = 200


#!Işık ekle

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

with open(resource_path("data.json"), "r", encoding="utf-8") as f:
    gameData = f.read()



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


reactor = Reactions()

class Particle:

    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,x_velocity=0,y_velocity=0,sh=1,lifeTime = -1):
        self.name = name
        self.pygame = pygame
        self.temp = max(-273.15 , min(temp,9500))
        self.sh = sh #Oz Isı
        self.mass = mass
        self.color = color
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.id = particleId
        self.lifeTime = lifeTime 
    #* Düzeldi    
    def draw(self,win,grid):
        self.pygame.draw.rect(win, self.color, (self.x, self.y, 3, 3))
        theGrid = grid[min(max(int(self.y//3),0),GRIDHEIGHT)][min(max(int(self.x//3),0),GRIDWIDTH)]
        if self not in theGrid:theGrid.append(self)

    #*Düzeldi
    def gravity(self,win,gravity,dt,grid,theGame):
        if self.y <= HEIGHT:
            downCell = grid[min(int(self.y//3)+1,GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
            if downCell and any(item.type in ("solid", "powder") or item.type == self.type for item in downCell):
                self.y_velocity = 0
                return
            
            gravity = int(round(gravity * dt * 15 / 3) * 3) 
            self.y_velocity += gravity
            if self.y_velocity >= 3:
                self.y_velocity = 3
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
            cell = grid[int(y)//3][min(int(x) //3, GRIDWIDTH)]
            if len(cell) >= 1 :
                return [True,(x,y),cell]
            else:
                return [False,0]
        return [False,0]


    def move(self,win,dt,grid):pass


class Nuclear(Particle):
    def __init__(self,name:str,particleId:int,pygame,x,y,temp,mass,color,x_velocity=250,y_velocity=250,lifeTime = HEIGHT):
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
            cell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
            self.x += math.cos(self.degree) * self.x_velocity * dt * 0.5
            self.y += math.sin(self.degree) * self.y_velocity * dt * 0.5
            self.x , self.y = int(round(self.x/3)*3) , int(round(self.y/3)*3)
            if self not in cell:
                cell.append(self)
                return cell





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
                part = Nuclear(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),tuple(particle["color"]))
                return part

            case "powder":
                part = Powder(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),tuple(particle["color"]))
                return part

            case "solid":
                part = Solid(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),tuple(particle["color"]))
                return part

            case "liquid":
                part = Liquid(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),tuple(particle["color"]))
                return part

            case "gas":
                part = Gas(particle["name"],id,pygame,x,y,int(particle["temp"]),int(particle["mass"]),tuple(particle["color"]))
                return part


            case _:
                pass





    def elementData(self,id):
        return self.veri["particles"][str(id)]


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
            downCell = grid[min(max(int(self.y//3)+1,0),GRIDHEIGHT)][min(max((int(self.x) //3,0)), GRIDWIDTH)]
            if len(downCell) > 0:
                gotoCell = grid[min(max(int(self.y//3+1),0),GRIDHEIGHT)][min(max((int(self.x) //3)+moveTo,0), GRIDWIDTH)]
                if len(gotoCell) > 0 and any(item.type in ("solid", "powder") or item.type == self.type for item in gotoCell):
                    moveTo *= -1
                gotoCell = grid[min(max(int(self.y//3+1),0),GRIDHEIGHT)][min(max((int(self.x) //3)+moveTo,0), GRIDWIDTH)]
                if len(gotoCell) > 0 and any(item.type in ("solid", "powder") or item.type == self.type for item in gotoCell):
                    moveTo *= 0
            else:moveTo *= 0

            self.x += int(moveTo*3)
            gotoX , gotoY = self.x//3 , self.y //3 
            cell = grid[min(max(int(gotoY),0),GRIDHEIGHT)][min(max(int(gotoX),0), GRIDWIDTH)]
            
            if self not in cell:
                cell.append(self)
                return cell


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
        theGrid = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
        if not self in theGrid:
            theGrid.append(self)            



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
        upCell = grid[min(int(self.y//3)-1,GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
        downCell = grid[min(int(self.y//3)+1,GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
        if len(upCell) == 0 and len(downCell) > 0:

            gotoCell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3)+moveTo, GRIDWIDTH)]
            if len(gotoCell) > 0:
                moveTo *= -1
            gotoCell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3)+moveTo, GRIDWIDTH)]
            if len(gotoCell) > 0:
                moveTo *= 0
        else:moveTo *= 0


        self.x += int(moveTo*3)
        cell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3) , GRIDWIDTH)]
        if len(cell) >1:
            if any(item.type == "powder" for item in cell):
                roadFound = False
                road = 0
                while not roadFound:
                    if len(grid[min(max(int(self.y//3)-road,0),GRIDHEIGHT)][min(max(int(self.x//3),0),GRIDWIDTH)]) <1:
                        roadFound = True
                        road*=3
                    else:
                        road+=1
                self.y -= road
                grid[min(max(int(self.y//3),0),GRIDHEIGHT)][min(max(int(self.x//3),0),GRIDWIDTH)].append(self)
            cell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]
            
        if self not in cell:
            cell.append(self)
            return cell


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
        value = 0 if value == 0 else int(math.copysign(max(1, round(abs(value) / 3)), value) * 3)
        self.y_velocity +=  value

        if self.y_velocity != value:
            self.y_velocity = value
        if len(grid[min(int(self.y//3)+int(value//3),GRIDHEIGHT)][min((int(self.x) //3), GRIDWIDTH)]) > 0:
            self.y_velocity = 0
            self.x += int(direction * 3)
            return

        self.y += self.y_velocity
        grid[min(max(int(self.y//3),0),GRIDHEIGHT)][min(max((int(self.x) //3+direction),0), GRIDWIDTH)]


    def move(self,win,dt,grid):
        moveTo = random.randint(0,1) * 2 - 1
        gotoCell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3)+moveTo, GRIDWIDTH)]
        if len(gotoCell) > 0:
            moveTo *= -1
        gotoCell = grid[min(int(self.y//3),GRIDHEIGHT)][min((int(self.x) //3)+moveTo, GRIDWIDTH)]
        if len(gotoCell) > 0:
            moveTo *= 0

        moveTo = int(moveTo*3)
        self.x += moveTo