import pygame
import random
from Spritesheet import SpriteSheet
from pygame import mixer
from enemy import Enemy

# инициализация pygame и mixer
mixer.init()
pygame.init()

# окно игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# определяем фон
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

# устанавливаем частоту кадров
clock = pygame.time.Clock()
FPS = 60

# загрузка музыки
pygame.mixer.music.load(r'C:\Users\Булат\Desktop\Game\music.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)
jump_fx = pygame.mixer.Sound(r'C:\Users\Булат\Desktop\Game\jump.mp3')
jump_fx.set_volume(0.5)
death_fx = pygame.mixer.Sound(r'C:\Users\Булат\Desktop\Game\death.mp3')
death_fx.set_volume(0.5)

# добавляем игровые переменные(гравитация)
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0

# определяем рамку
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

# определение шрифтов
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

# загрузка изображений
bg_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\bg.png').convert_alpha()
jumpy_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\jump.png').convert_alpha()
platform_image = pygame.image.load(r'C:\Users\Булат\Desktop\Game\wood.png').convert_alpha()
bird_sheet_img = pygame.image.load(r'C:\Users\Булат\Desktop\Game\bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)


# функция вывода текста
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# функция для рисования фона(нужно сделать, чтобы фон пролистывался, а не двигался с нами)
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

# функция дле подсчёта очков
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)

# класс игрока
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.flip = False
        self.vel_y = 0

    def move(self):
        # сбрасываем переменные
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # гравитация
        self.vel_y += GRAVITY
        dy += self.vel_y

        # нужно проверить не выходим ли за край экрана
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # проверяем столкновение с платформой
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # проверяем находимся внизу или вверху платформы
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_fx.play()



        # проверяем не отскочил ли игрок за верхнюю часть экрна
        if self.rect.top <= SCROLL_THRESH:
            # если игрок прыгает
            if self.vel_y < 0:
                scroll = -dy

        # обновляем положение прямоугольника
        self.rect.x += dx
        self.rect.y += dy + scroll

        # обновление маски
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))



# создаем класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        # перемещение платформы
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        # изменение направления платформы, если она вышла за пределы экрана
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_HEIGHT:
            self.direction *= -1
            self.move_counter = 0

        # обновляем положение платформы
        self.rect.y += scroll
        # проверяем не исчезла ли плафторма
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# создаем группы платформ
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# создаем стартовую платформу
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)

# добавили игрока
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# игровой цикл
run = True
while run:

    clock.tick(FPS)
    if game_over == False:
        scroll = jumpy.move()

        # рисуем фон
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # создаем платформы
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 1000:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)


        # обновляем платформы
        platform_group.update(scroll)

        # создаем врагов
        if len(enemy_group) == 0 and score > 1500:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        # обновление группы врагов
        enemy_group.update(scroll, SCREEN_WIDTH)

        # обновляем счёт
        if scroll > 0:
            score += scroll

        # рисуем игрока
        platform_group.draw(screen)
        enemy_group.draw(screen)
        jumpy.draw()


        # рисуем счёт
        draw_panel()

        # проверяем конец игры
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_fx.play()
        # проверяем столкновение с врагами
        if pygame.sprite.spritecollide(jumpy, enemy_group, False):
            if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()

    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            pygame.draw.rect(screen, BLACK, (0, 0, fade_counter, SCREEN_HEIGHT))
        else:
            draw_text('GAME OVER!', font_big, WHITE, 130, 200)
            draw_text('SCORE: ' + str(score), font_big, WHITE, 130, 250)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # сбросить настройки переменных
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            # нужно изменить положение игрока
            jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # перезагружаем платформы
            platform_group.empty()
            # создаем стартовую платформу
            platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
            platform_group.add(platform)


    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # обновляем окно отображения
    pygame.display.update()

pygame.quit()