import pygame
import sys
import math
import random

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

gun_width, gun_height = 20, 60
gun_x, gun_y = screen_width // 2, screen_height - gun_height // 2
gun_angle = 0  

bullets = []
enemies = []

enemy_shapes = ['square', 'triangle', 'circle']
enemy_colors = [RED, GREEN, BLUE]

score = 0
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_dx = math.sin(math.radians(-gun_angle))
                bullet_dy = -math.cos(math.radians(-gun_angle))
                bullet_x = gun_x + (gun_height // 2) * bullet_dx
                bullet_y = gun_y + (gun_height // 2) * bullet_dy
                new_bullet = pygame.Rect(bullet_x, bullet_y, 5, 5), (bullet_dx, bullet_dy)
                bullets.append(new_bullet)

    if random.random() < 0.01:  # 1% chance to spawn a new enemy each frame
        enemy_shape = random.choice(enemy_shapes)
        enemy_color = random.choice(enemy_colors)
        enemy_x = random.randint(0, screen_width)
        enemy_y = 0
        enemy_velocity = random.randint(1, 3)
        new_enemy = {'shape': enemy_shape, 'color': enemy_color, 'rect': pygame.Rect(enemy_x, enemy_y, 20, 20), 'velocity': enemy_velocity, 'visible': True}
        enemies.append(new_enemy)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gun_angle += 5  
    if keys[pygame.K_RIGHT]:
        gun_angle -= 5  

    screen.fill((0, 0, 0))  

    gun_surface = pygame.Surface((gun_width, gun_height), pygame.SRCALPHA)
    gun_rect = pygame.Rect(0, 0, gun_width, gun_height)
    pygame.draw.rect(gun_surface, WHITE, gun_rect)
    rotated_gun = pygame.transform.rotate(gun_surface, gun_angle)
    rotated_rect = rotated_gun.get_rect(center=(gun_x, gun_y))
    

    screen.blit(rotated_gun, rotated_rect)
    for bullet in bullets[:]:
        pygame.draw.rect(screen, WHITE, bullet[0])
        bullet[0].x += 5 * bullet[1][0]
        bullet[0].y += 5 * bullet[1][1]
        for enemy in enemies:
            if bullet[0].colliderect(enemy['rect']) and enemy['visible']:
                bullets.remove(bullet)
                enemy['visible'] = False
                score += 1
                break

    for enemy in enemies:
        if enemy['visible']:
            if enemy['shape'] == 'square':
                pygame.draw.rect(screen, enemy['color'], enemy['rect'], 2)
            elif enemy['shape'] == 'triangle':
                pygame.draw.polygon(screen, enemy['color'], [(enemy['rect'].x, enemy['rect'].y + enemy['rect'].height), (enemy['rect'].x + enemy['rect'].width // 2, enemy['rect'].y), (enemy['rect'].x + enemy['rect'].width, enemy['rect'].y + enemy['rect'].height)], 2)
            elif enemy['shape'] == 'circle':
                pygame.draw.circle(screen, enemy['color'], enemy['rect'].center, enemy['rect'].width // 2, 2)
            enemy['rect'].y += enemy['velocity']
           
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()