import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle / AABB / OBB Collision Comparison")

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# 플레이어(Rect 기반, 이동 가능)
player = pygame.Rect(100, 100, 120, 80)
player_angle = 0  # 플레이어는 회전하지 않음

# 중앙 회전 오브젝트
fixed_center = (WIDTH // 2, HEIGHT // 2)
fixed_width = 120
fixed_height = 80
fixed_angle = 0

move_speed = 5
base_rotation_speed = 1
fast_rotation_speed = 4

def get_rotated_corners(center, width, height, angle_deg):
    cx, cy = center
    rad = math.radians(angle_deg)

    hw = width / 2
    hh = height / 2

    corners = [
        (-hw, -hh),
        ( hw, -hh),
        ( hw,  hh),
        (-hw,  hh)
    ]

    rotated = []
    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        rotated.append((cx + rx, cy + ry))

    return rotated

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def normalize(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2)
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)

def get_axes(corners):
    axes = []
    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]

        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])
        axes.append(normalize(normal))
    return axes

def project(corners, axis):
    values = [dot(point, axis) for point in corners]
    return min(values), max(values)

def sat_collision(c1, c2):
    axes = get_axes(c1) + get_axes(c2)

    for axis in axes:
        min1, max1 = project(c1, axis)
        min2, max2 = project(c2, axis)

        if max1 < min2 or max2 < min1:
            return False
    return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 플레이어 이동
    if keys[pygame.K_LEFT]:
        player.x -= move_speed
    if keys[pygame.K_RIGHT]:
        player.x += move_speed
    if keys[pygame.K_UP]:
        player.y -= move_speed
    if keys[pygame.K_DOWN]:
        player.y += move_speed

    # 회전 속도 조절
    if keys[pygame.K_z]:
        fixed_angle += fast_rotation_speed
    else:
        fixed_angle += base_rotation_speed

    screen.fill(WHITE)

    # ----------------------------
    # OBB 계산
    # ----------------------------
    player_corners = get_rotated_corners(player.center, player.width, player.height, player_angle)
    fixed_corners = get_rotated_corners(fixed_center, fixed_width, fixed_height, fixed_angle)

    obb_collision = sat_collision(player_corners, fixed_corners)

    # ----------------------------
    # AABB 계산 (OBB와 중심 위치 동일)
    # ----------------------------
    player_aabb = player.copy()

    fixed_aabb = pygame.Rect(0, 0, fixed_width, fixed_height)
    fixed_aabb.center = fixed_center

    aabb_collision = player_aabb.colliderect(fixed_aabb)

    # ----------------------------
    # 원형 충돌 계산
    # ----------------------------
    player_center = player.center
    player_radius = player.width // 2
    fixed_radius = fixed_width // 2

    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    circle_collision = distance <= (player_radius + fixed_radius)

    # ----------------------------
    # 본체 그리기
    # ----------------------------
    pygame.draw.polygon(screen, GRAY, player_corners)
    pygame.draw.polygon(screen, GRAY, fixed_corners)

    # 원형 Bounding Box (파랑)
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 2)

    # AABB (빨강)
    pygame.draw.rect(screen, RED, player_aabb, 2)
    pygame.draw.rect(screen, RED, fixed_aabb, 2)

    # OBB (초록)
    pygame.draw.polygon(screen, GREEN, player_corners, 2)
    pygame.draw.polygon(screen, GREEN, fixed_corners, 2)

    # 중심점
    pygame.draw.circle(screen, BLUE, player_center, 5)
    pygame.draw.circle(screen, BLUE, fixed_center, 5)

    # 상태 텍스트
    circle_text = "Circle: HIT" if circle_collision else "Circle: SAFE"
    aabb_text = "AABB: HIT" if aabb_collision else "AABB: SAFE"
    obb_text = "OBB: HIT" if obb_collision else "OBB: SAFE"

    screen.blit(font.render(circle_text, True, BLACK), (20, 20))
    screen.blit(font.render(aabb_text, True, BLACK), (20, 55))
    screen.blit(font.render(obb_text, True, BLACK), (20, 90))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()