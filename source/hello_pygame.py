import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
running = True

# 원의 시작 위치
x = 400
y = 300

# 이동 속도와 반지름
speed = 5
radius = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 현재 눌린 키 확인
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # 경계선 밖으로 못 나가게 제한
    if x < radius:
        x = radius
    if x > 800 - radius:
        x = 800 - radius
    if y < radius:
        y = radius
    if y > 600 - radius:
        y = 600 - radius

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()