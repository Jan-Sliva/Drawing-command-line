import pygame, os
import pygame._sdl2.touch

ROZMERY = (500, 500)
TLOUŠŤKA = 2
FOLDER = "test"

screen = pygame.display.set_mode(ROZMERY)
screen.fill((255, 255, 255))


isPressed = False
drawTheLine = False
running = True

index = 0
soubory = os.listdir(FOLDER)
while (str(index) + ".png") in soubory:
    index += 1


while running:
  for event in pygame.event.get():
    if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
        isPressed = True
        drawTheLine = False
    elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
        isPressed = False
    elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 3):
        pygame.image.save(screen, os.path.join(FOLDER, str(index) + ".png"))
        screen.fill((255, 255, 255))
        index +=1
        soubory = os.listdir(FOLDER)
        while (str(index) + ".png") in soubory:
            index += 1
    elif event.type == pygame.QUIT:
        running = False

    if event.type == pygame.MOUSEMOTION and isPressed == True:
        (x,y) = pygame.mouse.get_pos()
        if drawTheLine:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (lX, lY), TLOUŠŤKA)
        else:
            drawTheLine = True
        lX, lY = x, y
  pygame.display.flip()
