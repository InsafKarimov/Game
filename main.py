import pygame

#инициализация pygame
pygame.init()

#окно игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
#определяем фон

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

#определяем рамку
WHITE = (255, 255, 255)

#загрузка изображений
bg_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\bg.png').convert_alpha()
jumpy_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\jump.png').convert_alpha()

#класс игрока
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
    def draw(self):
        screen.blit(self.image, (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)


#игровой цикл
run = True
while run:

    #рисуем фон
    screen.blit(bg_image, (0, 0))

    #рисуем игрока
    jumpy.draw()

    #обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #обновляем окно отображения
    pygame.display.update()

pygame.quit()