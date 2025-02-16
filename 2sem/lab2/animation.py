import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Поздоровкин Кирилл Алексеевич")

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

class Shape:
    def __init__(self, shape_type, x, y, size, speed):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = random_color()

    def draw(self, surface):
        if self.shape_type == "square":
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape_type == "rectangle":
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size / 2))
        elif self.shape_type == "circle":
            pygame.draw.circle(surface, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
        elif self.shape_type == "triangle":
            pygame.draw.polygon(surface, self.color, [
                (self.x, self.y + self.size), (self.x + self.size, self.y + self.size), (self.x + self.size // 2, self.y)
            ])

    def move(self, width):
        self.x += self.speed
        if self.x <= 0 or self.x + self.size >= width:
            self.speed = -self.speed
            self.color = random_color()

    def check_click(self, mouse_pos):
        if self.shape_type in ["square", "rectangle"]:
            if self.x <= mouse_pos[0] <= self.x + self.size and self.y <= mouse_pos[1] <= self.y + self.size:
                self.color = random_color()
        elif self.shape_type == "circle":
            if (mouse_pos[0] - (self.x + self.size // 2)) ** 2 + (mouse_pos[1] - (self.y + self.size // 2)) ** 2 <= (self.size // 2) ** 2:
                self.color = random_color()
        elif self.shape_type == "triangle":
            if self.x <= mouse_pos[0] <= self.x + self.size and self.y <= mouse_pos[1] <= self.y + self.size:
                self.color = random_color()

shapes = [
    Shape("square", 100, 100, 50, 3),
    Shape("rectangle", 200, 200, 50, 4),
    Shape("circle", 300, 300, 50, 5),
    Shape("triangle", 400, 400, 50, 6),
]

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))
    width, height = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE: # Событие - изменение размера окна
            width, height = event.w, event.h
        elif event.type == pygame.MOUSEBUTTONDOWN: # Событие - клик мыши
            for shape in shapes:
                shape.check_click(event.pos)

    for shape in shapes:
        shape.move(width)
        shape.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
