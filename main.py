import pygame

#инициализация pygame
pygame.init()

#окно игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
#определяем фон


screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')
bg_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\bg.png').convert_alpha()

#игровой цикл
run = True
while run:

    #рисуем фон
    screen.blit(bg_image, (0, 0))

    #обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #обновляем окно отображения
    pygame.display.update()

pygame.quit()