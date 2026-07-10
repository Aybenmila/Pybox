import pygame
import backend
import asyncio




async def mainGame():


    #!ViewMode Ekle
    #!Gaz ve Light Ekle ekle
    #!Sıcaklık ve ısı sistemini kur


            

    async def mouseCreate():
        x, y = pygame.mouse.get_pos()
        x,y = x - cursorWidth//2 , y - cursorHeight //2
        for i in range(0,cursorHeight+1):
            newY = y + i
            for j in range(0,cursorWidth+1):
                newX = x + j
                occupied = False

                if len(grid[max(0, min(int(newY//3),GRIDHEIGHT ))][max(0, min(int(newX//3), GRIDWIDTH))]) > 0:occupied = True

                if not occupied:
                    part = game.spawner(selected, newX, newY, pygame)
                    parts.append(part)

                newX = x
            newY = y

    async def mouseDelete():
        x, y = pygame.mouse.get_pos()
        x,y = x - cursorWidth//2 , y - cursorHeight //2
        for i in range(0,cursorHeight+1):
            newY = y+i
            for j in range(0,cursorWidth+1):
                newX = x+j

                delete.extend(grid[max(0, min(int(newY//3),GRIDHEIGHT ))][max(0, min(int(newX//3), GRIDWIDTH))])




    #! INIT
    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    GRIDWIDTH = 267 
    GRIDHEIGHT = 200

    cursorWidth = 3
    cursorHeight = 3



    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pybox")
    pygame.mouse.set_visible(False)

    stopped = False
    running = True
    parts = []
    font = pygame.font.SysFont("Arial", 24)



    clock = pygame.time.Clock()
    game = backend.Game(9.98,60)
    delete = []
    selected = 1


    #! Testler
    #* Stres testi
    # for _ in range(4000):
    #     proton = backend.Nuclear("proton",2,pygame,GRIDHEIGHT,150,24,1,(255, 0, 0))
    #     electron = backend.Nuclear("electron",1,pygame,GRIDHEIGHT,450,24,1,(255, 255, 255))

    #     parts.append(proton)
    #     parts.append(electron)

    #* Tek particle testi
    # electron = backend.Nuclear(pygame,GRIDWIDTH,GRIDHEIGHT,24,1,(255, 255, 255))
    # parts.append(electron)

    #* Tabak
    # for i in range(300,500):
    #     iron = backend.Solid("iron",5,pygame,i,300,24,1,(255,32,13))
    #     parts.append(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,300,i,24,1,(255,32,13))
    #     parts.append(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,500,i,24,1,(255,32,13))
    #     parts.append(iron)


    #* Blok
    # for i in range(300,304):
    #     for j in range(250,300):
    #         iron = backend.Solid("iron",5,pygame,j,i,24,1,(255,32,13))
    #         parts.append(iron)


    while running:
        grid = [[[] for _ in range(-5,GRIDWIDTH)] for _ in range(-5,GRIDHEIGHT)]
        saat = clock.tick(game.tick)
        DT = saat / 1000
        win.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    selected += 1

                    if selected > 6:
                        selected = 1

                if event.key == pygame.K_LSHIFT:
                    cursorHeight = int(cursorHeight *1.5)
                    cursorWidth = int(cursorWidth *1.5)
                
                if event.key == pygame.K_SPACE:
                    stopped = not stopped


            if cursorHeight > 216 or cursorWidth > 216:
                cursorHeight , cursorWidth = 3,3



                

            
        
        
        
        
        
        for part in parts:
            part.draw(win,grid)
            if not stopped:
                if part.type != "solid":
                    part.gravity(win,game.gravity,DT,grid)
                    part.move(win,DT,grid)

                    if 0 > part.x or part.x >800:
                        try:
                            delete.append(part)
                        except:pass

                    if 0 > part.y or part.y >600:
                        try:
                            delete.append(part)
                        except:pass
                

                    if part.checkLifeTime():
                        delete.append(part)


                    result = part.checkCollision(grid)
                    if result[0]:
                        synthesis = []
                        data = game.reaction(result[2])
                        # heat = game.heat(result[2])
                        match data[0][0][0]:
                            case "NEUTSPWN":
                                part = game.spawner(data[0][0][1],result[1][0],result[1][1],pygame)
                                parts.append(part)
                                synthesis.append(part)
                                delete = [x for x in data[1] if x not in synthesis]






                            case "0":pass
                            case _:pass
            

                    

        if pygame.mouse.get_pressed()[0]:
            asyncio.create_task(mouseCreate())


        if pygame.mouse.get_pressed()[2]:
            asyncio.create_task(mouseDelete())
            

        for part in delete:
            try:parts.remove(part)
            except:pass

        delete = []





        # pygame.draw.rect(win,(111, 112, 106),( cursorHeight,cursorWidth))

        cursor = pygame.Surface((cursorWidth,cursorHeight))
        cursor.set_alpha(64)
        cursor.fill((255,255,255))
        win.blit(cursor,(pygame.mouse.get_pos()[0]-cursorWidth//2,pygame.mouse.get_pos()[1]-cursorHeight//2,))
        
        win.blit(font.render(f"Particle:{len(parts)} , FPS : {int(clock.get_fps())}", True, (255, 255, 255)), (0, 0))
        win.blit(font.render(f"selected particle:{game.elementData(selected)["name"]}",True,(255,255,255)),(0,20))
        
        pygame.display.flip()

        await asyncio.sleep(0)

        

    pygame.quit()
    

asyncio.run(mainGame())