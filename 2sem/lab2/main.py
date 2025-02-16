import pygame
import random
pygame.init()

screen=pygame.display.set_mode((800,600),pygame.RESIZABLE)
screen.fill((255,255,255))
pygame.display.set_caption('Первая программа в pygame')

pygame.draw.circle(screen,'red',[200,100],30,width=0)
pygame.draw.circle(screen,[255,154,13],[100,400],50,width=15)
pygame.draw.circle(screen,'#FF5E54',[400,300],100,width=5)

pygame.draw.rect(screen, 'yellow', [400,20,300,200],0)

for i in range(5):
    top=random.randint(10,700)
    left=random.randint(10,500)
    w=random.randint(10,200)
    h=random.randint(10,100)
    color=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    pygame.draw.rect(screen,color,[top,left,w,h],4)

house_x, house_y = 400, 400
roof_top = (house_x, 300)
roof_left = (house_x - 100, house_y)
roof_right = (house_x + 100, house_y)
pygame.draw.polygon(screen, 'brown', [roof_left, roof_top, roof_right])

pygame.draw.rect(screen, 'blue', [roof_left[0], house_y, 200, 200])
pygame.draw.rect(screen, 'black', [house_x - 30, house_y + 100, 60, 100])

dots=[
    [221,432],[225,331],[133,342],[141,310],
    [51,230],[74,217],[58,153],[114,164],
    [123,135],[176,190],[159,77],[193,93],
    [230,28],[267,93],[301,171],[284,190],
    [327,153],[336,164],[402,153],[386,217],
    [409,230],[319,310],[327,342],[331,432],
    [237,432]
]
pygame.draw.lines(screen,'green',True,dots,2)

apple=pygame.image.load('apple.png')
screen.blit(apple,[400,450])
pygame.display.flip()

pygame.time.delay(2000)
pygame.draw.rect(screen,'white',[400,450,100,100])
screen.blit(apple,[600,450])

pygame.display.flip()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
pygame.quit()
