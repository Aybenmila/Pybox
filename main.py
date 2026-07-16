import pygame
import backend




def mainGame():
#region INIT
    #! INIT
    pygame.init()
    WIDTH = 900
    HEIGHT = 600

    GRIDWIDTH = 300
    GRIDHEIGHT = 200
    CELLSIZE = 3

    cursorWidth = 3
    cursorHeight = 3

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pybox")
    pygame.mouse.set_visible(False)

    tempParts = []
    drawThermal = False
    drawGrids = False
    drawHGrids = False
    drawVGrids = False
    stopped = False
    running = True
    parts = set()
    font = pygame.font.SysFont("Arial", 24)



    clock = pygame.time.Clock()
    game = backend.Game(9.98,60,1.185)
    delete = []
    selected = 1

    backend.init(WIDTH,HEIGHT,GRIDWIDTH,GRIDHEIGHT,CELLSIZE)

#endregion
    
    def mouseCreate():
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
                    parts.add(part)
                    theGrid.append(part)

    def mouseDelete():
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
#region TestDraws

    # #! Testler
    # # * Stres testi
    # for _ in range(4000):
    #     proton = backend.Nuclear("proton",2,pygame,300,150,21,1,(255, 0, 0))
    #     electron = backend.Nuclear("electron",1,pygame,300,450,24,1,(255, 255, 255))

    #     parts.add(proton)
    #     parts.add(electron)

    # * Tek particle testi
    # electron = backend.Nuclear("electron",1,pygame,300,450,24,1,(255, 255, 255))
    # parts.add(electron)

    # # * Tabak
    # for i in range(300,500):
    #     iron = backend.Solid("iron",5,pygame,i,300,24,1,(255,32,13))
    #     parts.add(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,300,i,24,1,(255,32,13))
    #     parts.add(iron)

    # for i in range(250,300):
    #     iron = backend.Solid("iron",5,pygame,500,i,24,1,(255,32,13))
    #     parts.add(iron)


    # # * Blok
    # for i in range(300,304):
    #     for j in range(250,300):
    #         iron = backend.Solid("iron",5,pygame,j,i,24,1,(255,32,13))
    #         parts.add(iron)

#endregion
#region MainLoop
    while running:
        grid = [[[] for _ in range(0,GRIDWIDTH+1)] for _ in range(0,GRIDHEIGHT+1)]
        saat = clock.tick(game.tick)
        DT = saat / 1000
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    #region Keyboard Input
            if event.type == pygame.KEYDOWN:

                match event.key:
                    #*Change Particle
                    case pygame.K_TAB:
                        selected += 1

                        if selected > 8:
                            selected = 1
                    #*Change CursorSize
                    case  pygame.K_LSHIFT  | pygame.K_RSHIFT:
                        cursorHeight = int(cursorHeight *1.5)
                        cursorWidth = int(cursorWidth *1.5)
                    #*Start Stop Game
                    case pygame.K_SPACE:
                        stopped = not stopped
                    #*Clear Canvas
                    case pygame.K_r:
                        grid = [[[] for _ in range(-5,GRIDWIDTH)] for _ in range(-5,GRIDHEIGHT)]
                        parts.clear()
                        delete.clear()
                    #*Draw Horizontal Grids
                    case pygame.K_1:
                        drawHGrids = not drawHGrids
                    #*Draw Vertical Grids
                    case pygame.K_2:
                        drawVGrids = not drawVGrids
                    #*Draw Grids
                    case pygame.K_g:
                        drawGrids = not drawGrids
                    #*Draw Thermal
                    case pygame.K_t:
                        drawThermal = not drawThermal

                    case _:pass
    #endregion
            
            if cursorHeight > 216 or cursorWidth > 216:
                cursorHeight , cursorWidth = 3,3

#region Part functions
        for part in list(parts):
            if not drawGrids and not drawThermal:part.draw(win,grid);part.drawGlow(win)


        for part in list(parts):
            if not stopped:
                part.move(win,DT,grid)
                if  part.type !="solid":
                    part.gravity(win,game.gravity,DT,grid,game)

                    if 3 > part.x or part.x >WIDTH-3:parts.discard(part)

                    if 3 > part.y or part.y >HEIGHT-3:parts.discard(part)

                

                    if part.checkLifeTime():
                        delete.append(part)

        for part in list(parts):
            if not stopped and part.type != "solid":
                result = part.checkCollision(grid)
                if result[0]:
                    synthesis = []
                    data = game.reaction(result[2])
                    match data[0][0][0]:
                        case "NEUTSPAWN":
                            part = game.spawner(data[0][0][1],result[1][0],result[1][1],pygame)
                            tempParts.append(part)
                            synthesis.append(part)
                            delete = [x for x in data[1] if x not in synthesis]
                        
                        case "0":pass
                        case _:pass
                    for data in delete:
                        try:
                            parts.discard(data)
                        except:pass
        parts.update(p for p in tempParts if p is not None)
        tempParts.clear()
#endregion
#region MouseFunctions
        if pygame.mouse.get_pressed()[0]:
            mouseCreate()


        if pygame.mouse.get_pressed()[2]:
            mouseDelete()
#endRegion
        
        #Delete
        for part in delete:
            try:parts.discard(part)
            except:pass

        delete = []





        # pygame.draw.rect(win,(111, 112, 106),( cursorHeight,cursorWidth))
#region ViewMods
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
        
        if drawThermal:
            for part in list(parts):
                part.color = (int(min(255,max(part.temp,50))),0,0)
                print(part.color)
                pygame.draw.rect(win,part.color,(part.x,part.y,3,3))
            


        cursor = pygame.Surface((cursorWidth,cursorHeight))
        cursor.set_alpha(64)
        cursor.fill((255,255,255))

        win.blit(cursor,(pygame.mouse.get_pos()[0]-cursorWidth//2,pygame.mouse.get_pos()[1]-cursorHeight//2))
        win.blit(font.render(f"Particle:{len(parts)} , FPS : {int(clock.get_fps())} cursor : {cursorHeight}", True, (255, 255, 255)), (0, 0))
        win.blit(font.render(f"selected particle:{game.particleData(selected)["name"]}",True,(255,255,255)),(0,20))
#endregion
        
        
        
        pygame.display.flip()

        for row in grid:
            for cell in row:
                cell.clear()
                

    pygame.quit()
#endregion

if __name__ == "__main__":mainGame()