import pygame

pygame.init()

window_width = 800
window_height = 600
fon = 'fon.png'  # изображение должно быть в том же каталоге, что и код на питоне
player_image = 'invoker.png'  # изображение спрайта

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра v1.0")

img_fon = pygame.image.load(fon)
back_fon = pygame.transform.scale(img_fon, (window_width, window_height))
sdvig_fona = 0  # сдвиг фона

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

# Создание игрока
hero = Player(player_image)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # пришло ли событие нажатия на крестик
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
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero.x_speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                hero.y_speed = 0

    hero.update()

    sdvig_fona %= window_width
    window.blit(back_fon, (sdvig_fona, 0))
    window.blit(back_fon, (sdvig_fona - window_width, 0))  # рисуем фон слева от сдвига

    window.blit(hero.image, hero.rect)  # отрисовываем персонажа поверх фона

    pygame.display.update()  # обновилось содержимое окна
    clock.tick(60)

pygame.quit()  # закрыть окно крестиком
