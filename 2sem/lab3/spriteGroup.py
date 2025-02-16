import pygame
import random

pygame.init()

window_width = 800
window_height = 600
fon = 'fon.png'
player_image = 'invoker.png'
enemy_image = 'enemy.png'
arrow_image = 'arrow.png'

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Финальная игра")

img_fon = pygame.image.load(fon)
back_fon = pygame.transform.scale(img_fon, (window_width, window_height))
sdvig_fona = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250, x_speed=0, y_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)  # загрузка героя из файла
        self.image = pygame.transform.scale(self.image, (120, 120))  # изменение размера спрайта
        self.rect = self.image.get_rect()

        # Ставим персонажа в переданную точку (x, y):
        self.rect.x = hero_x
        self.rect.y = hero_y

        # Создаем скорость движения спрайта:
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        """
        Перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Границы экрана и сдвиг фона
        global sdvig_fona
        if self.rect.right >= window_width:  # если достиг правого края
            self.rect.right = window_width
            sdvig_fona -= self.x_speed  # двигаем фон влево
        if self.rect.left <= 0:  # если достиг левого края
            self.rect.left = 0
            sdvig_fona -= self.x_speed  # двигаем фон вправо

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Если вышел за границы – возвращаем
            self.rect.left = window_width

# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (70, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10  # Скорость стрелы

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > window_width:  # Удаляем, если улетела за экран
            self.kill()

def createEnemy():
    return Enemy(enemy_image, 600, random.randint(100, 500), random.randint(1, 5))

hero = Player(player_image)
enemy1 = createEnemy()
enemy2 = createEnemy()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

all_sprites.add(hero, enemy1, enemy2)
enemies.add(enemy1, enemy2)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.x_speed = -5
            if event.key == pygame.K_RIGHT:
                hero.x_speed = 5
            if event.key == pygame.K_UP:
                hero.y_speed = -5
            if event.key == pygame.K_DOWN:
                hero.y_speed = 5
            if event.key == pygame.K_SPACE:  # Создание стрелы
                arrow = Arrow(arrow_image, hero.rect.right, hero.rect.centery)
                all_sprites.add(arrow)
                arrows.add(arrow)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero.x_speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                hero.y_speed = 0

    all_sprites.update()

    window.fill((0, 0, 0))

    for arrow in arrows:
        hits = pygame.sprite.spritecollide(arrow, enemies, True)
        if hits:
            arrow.kill()
            newEnemy = createEnemy()
            all_sprites.add(newEnemy)
            enemies.add(newEnemy)

    sdvig_fona = sdvig_fona % window_width
    window.blit(back_fon, (sdvig_fona, 0))
    window.blit(back_fon, (sdvig_fona - window_width, 0))

    all_sprites.draw(window)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
