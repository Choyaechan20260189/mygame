import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
running = True

# 원 위치
x = 400
y = 300
speed = 10
radius = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 🔥 이전 위치 저장 (충돌 시 되돌리기용)
    prev_x = x
    prev_y = y

    # 🔥 키 입력 처리 (동시 입력 가능)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed

    # 🔥 충돌 체크 (화면 밖 나가면 원위치)
    if x - radius < 0 or x + radius > 800 or y - radius < 0 or y + radius > 600:
        x = prev_x
        y = prev_y

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()