import pygame


class Circle:
    def __init__(self, x, y, dx, dy, color, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = radius

    def getPos(self):
        return self.x, self.y


running = True


def main():
    global running, screen

    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("First Project")

    circle = Circle(100, 100, 10, 10, (255, 255, 0), 15)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            screen.fill((20, 20, 20))
            drawCircle(circle)
            pygame.display.update()


def drawCircle(circle):
    if running:
        pygame.draw.circle(screen, circle.color, (circle.x, circle.y), circle.radius)
        circle.x += circle.dx
        circle.y += circle.dy
        tryChangeDir(circle)


def tryChangeDir(circle):
    if circle.x - circle.radius < 0 or circle.x + circle.radius > screen.get_width():
        circle.dx *= -1
    if circle.y - circle.radius < 0 or circle.y + circle.radius > screen.get_height():
        circle.dy *= -1


if __name__ == "__main__":
    main()
