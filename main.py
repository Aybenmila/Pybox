import pygame
import backend
import asyncio




async def mainGame():

    #! INIT
    pygame.init()

    WIDTH = 900
    HEIGHT = 600

    GRIDWIDTH = 300
    GRIDHEIGHT = 200

    cursorWidth = 3
    cursorHeight = 3



    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pybox")
    pygame.mouse.set_visible(False)

    tempParts = []
    drawGrids = False
    drawHGrids = False
    drawVGrids = False
    stopped = False
    running = True
    parts = []
    font = pygame.font.SysFont("Arial", 24)



    clock = pygame.time.Clock()
    game = backend.Game(9.98,60,1.185)
    delete = []
    selected = 1


    async def mouseCreate():
        x, y = pygame.mouse.get_pos()
        x, y = x - cursorWidth // 2, y - cursorHeight // 2
        for i in range(0, cursorHeight // 3):
            newY = y + (i * 3)
            for j in range(0, cursorWidth // 3):
                newX = x + (j * 3)

                # Önce hedef koordinatı hesapla
                spawnX = int(round(newX / 3) * 3)
                spawnY = int(round(newY / 3) * 3)

                theGrid = grid[max(0, min(spawnY // 3, GRIDHEIGHT))][max(0, min(spawnX // 3, GRIDWIDTH))]
                
                if len(theGrid) == 0:
                    part = game.spawner(selected, spawnX, spawnY, pygame)
                    parts.append(part)
                    theGrid.append(part)


    async def mouseDelete():
        x, y = pygame.mouse.get_pos()

        x -= cursorWidth // 2
        y -= cursorHeight // 2

        start_x = max(0, x // 3)
        end_x = min(GRIDWIDTH, (x + cursorWidth) // 3)

        start_y = max(0, y // 3)
        end_y = min(GRIDHEIGHT, (y + cursorHeight) // 3)

        for gy in range(start_y, end_y + 1):
            row = grid[gy]
            for gx in range(start_x, end_x + 1):
                delete.extend(row[gx])
                row[gx].clear()







    # #! Testler
    # # * Stres testi
    # for _ in range(4000):
    #     proton = backend.Nuclear("proton",2,pygame,300,150,21,1,(255, 0, 0))
    #     electron = backend.Nuclear("electron",1,pygame,300,450,24,1,(255, 255, 255))

    #     parts.append(proton)
    #     parts.append(electron)

    # * Tek particle testi
    # electron = backend.Nuclear("electron",1,pygame,300,450,24,1,(255, 255, 255))
    # parts.append(electron)

    # # * Tabak
    # for i in range(300,500):
    #     iron = backend.Solid("iron",5,pygame,i,300,24,1,(255,32,13))
    #     parts.append(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,300,i,24,1,(255,32,13))
    #     parts.append(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,500,i,24,1,(255,32,13))
    #     parts.append(iron)


    # # * Blok
    # for i in range(300,304):
    #     for j in range(250,300):
    #         iron = backend.Solid("iron",5,pygame,j,i,24,1,(255,32,13))
    #         parts.append(iron)


    while running:
        grid = [[[] for _ in range(0,GRIDWIDTH+1)] for _ in range(0,GRIDHEIGHT+1)]
        saat = clock.tick(game.tick)
        DT = saat / 1000
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    selected += 1

                    if selected > 7:
                        selected = 1

                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    cursorHeight = int(cursorHeight *1.5)
                    cursorWidth = int(cursorWidth *1.5)
                
                if event.key == pygame.K_SPACE:
                    stopped = not stopped

                if event.key == pygame.K_r:
                    grid = [[[] for _ in range(-5,GRIDWIDTH)] for _ in range(-5,GRIDHEIGHT)]
                    parts.clear()
                    delete.clear()



                if event.key == pygame.K_1:
                    drawHGrids = not drawHGrids

                if event.key == pygame.K_2:
                    drawVGrids = not drawVGrids



                if event.key == pygame.K_g:
                    drawGrids = not drawGrids


            if cursorHeight > 216 or cursorWidth > 216:
                cursorHeight , cursorWidth = 3,3

        for part in parts:
            if not drawGrids:part.draw(win,grid);part.drawGlow(win)

        for part in parts:
            if not stopped:
                part.gravity(win,game.gravity,DT,grid,game)
                part.move(win,DT,grid)

                if 3 > part.x or part.x >WIDTH-3:
                    try:
                        parts.remove(part)
                    except:pass

                if 3 > part.y or part.y >HEIGHT-3:
                    try:
                        parts.remove(part)
                    except:pass
            

                if part.checkLifeTime():
                    delete.append(part)


        for part in parts:
            if not stopped:
                result = part.checkCollision(grid)
                if result[0]:
                    synthesis = []
                    data = game.reaction(result[2])
                    # heat = game.heat(result[2])
                    match data[0][0][0]:
                        case "NEUTSPWN":
                            part = game.spawner(data[0][0][1],result[1][0],result[1][1],pygame)
                            tempParts.append(part)
                            synthesis.append(part)
                            delete = [x for x in data[1] if x not in synthesis]






                        case "0":pass
                        case _:pass
        parts.extend(part for part in tempParts)
        tempParts.clear()
            

                    

        if pygame.mouse.get_pressed()[0]:
            asyncio.create_task(mouseCreate())


        if pygame.mouse.get_pressed()[2]:
            asyncio.create_task(mouseDelete())
            

        for part in delete:
            try:parts.remove(part)
            except:pass

        delete = []





        # pygame.draw.rect(win,(111, 112, 106),( cursorHeight,cursorWidth))

        if drawVGrids:
            for i in range(0,WIDTH,3):
                pygame.draw.line(win,(255,0,0),(i,0),(i,HEIGHT))
        
        if drawHGrids:
            for i in range(0,HEIGHT,3):
                pygame.draw.line(win,(255,0,0),(0,i),(WIDTH,i))
                
        if drawGrids:
            index_map = {
            (y, x)
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell}
            for indexies in index_map:
                pygame.draw.rect(win,(255,255,255),(indexies[1]*3,indexies[0]*3,3,3))
            


        cursor = pygame.Surface((cursorWidth,cursorHeight))
        cursor.set_alpha(64)
        cursor.fill((255,255,255))

        win.blit(cursor,(pygame.mouse.get_pos()[0]-cursorWidth//2,pygame.mouse.get_pos()[1]-cursorHeight//2))
        win.blit(font.render(f"Particle:{len(parts)} , FPS : {int(clock.get_fps())}", True, (255, 255, 255)), (0, 0))
        win.blit(font.render(f"selected particle:{game.elementData(selected)["name"]}",True,(255,255,255)),(0,20))
        
        pygame.display.flip()

        

        await asyncio.sleep(0)

        

    pygame.quit()
    

asyncio.run(mainGame())