import pygame
import backend

pygame.init()

WIDTH = 800
HEIGHT = 600



#!ViewMode Ekle
#!Sıvı ve  Gaz ekle
#!Daha fazla element ekle
#!Sıcaklık ve ısı sistemini kur
#!Json ile tepkime datalarını tut

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sandbox")

running = True
parts = []
font = pygame.font.SysFont("Arial", 24)

#!Stres testi
# for _ in range(4000):
#     proton = backend.Nuclear("proton",2,pygame,200,150,24,1,(255, 0, 0))
#     electron = backend.Nuclear("electron",1,pygame,200,450,24,1,(255, 255, 255))

#     parts.append(proton)
#     parts.append(electron)

#* Tek particle testi
# electron = backend.Nuclear(pygame,267,200,24,1,(255, 255, 255))
# parts.append(electron)



clock = pygame.time.Clock()
game = backend.Game(9.98,60)
delete = []
selected = 1





while running:
    grid = [[[] for _ in range(-5,267)] for _ in range(-5,200)]
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

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()

        occupied = False

        for part in parts:
            if int(part.x // 3) == int(x // 3) and int(part.y // 3) == int(y // 3):
                occupied = True
                break

        if not occupied:
            part = game.spawner(selected, x, y, pygame)
            parts.append(part)
            


        
    
    
    
    
    
    for part in parts:
        part.gravity(win,game.gravity,DT,grid)
        part.move(win,DT,grid)
        part.draw(win)
        
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
                
        # if part.type == "powder":
        #     print(part.y_velocity)

    if pygame.mouse.get_pressed()[2]:
        delete.extend(grid[max(0, min(pygame.mouse.get_pos()[1]//3, 200))][max(0, min(pygame.mouse.get_pos()[0]//3, 267))])

    for part in delete:
        try:parts.remove(part)
        except:pass

    delete = []





    
    win.blit(font.render(f"Particle:{len(parts)}",True,(255,255,255)),(0,0))
    win.blit(font.render(f"selected particle:{game.elementData(selected)["name"]}",True,(255,255,255)),(0,20))
    pygame.display.flip()


    

pygame.quit()