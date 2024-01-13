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
killer_enemies = []

enemy_shapes = ['square', 'triangle', 'circle']
enemy_colors = [RED, GREEN, BLUE]

boss = None
multishot = False
multishot_start_time = 0

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

paused = False
paused_font = pygame.font.Font(None, 72)  

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
                bullet_char = random.choice(alphabet)  # Assign a random character from the alphabet to the bullet
                new_bullet = pygame.Rect(bullet_x, bullet_y, 5, 5), (bullet_dx, bullet_dy), bullet_char
                bullets.append(new_bullet)
            if multishot:
                    bullet_dx_left = math.sin(math.radians(-gun_angle - 10))
                    bullet_dy_left = -math.cos(math.radians(-gun_angle - 10))
                    bullet_x_left = gun_x + (gun_height // 2) * bullet_dx_left
                    bullet_y_left = gun_y + (gun_height // 2) * bullet_dy_left
                    new_bullet_left = pygame.Rect(bullet_x_left, bullet_y_left, 5, 5), (bullet_dx_left, bullet_dy_left), random.choice(alphabet)
                    bullets.append(new_bullet_left)
                    bullet_dx_right = math.sin(math.radians(-gun_angle + 10))
                    bullet_dy_right = -math.cos(math.radians(-gun_angle + 10))
                    bullet_x_right = gun_x + (gun_height // 2) * bullet_dx_right
                    bullet_y_right = gun_y + (gun_height // 2) * bullet_dy_right
                    new_bullet_right = pygame.Rect(bullet_x_right, bullet_y_right, 5, 5), (bullet_dx_right, bullet_dy_right), random.choice(alphabet)
                    bullets.append(new_bullet_right)
            elif event.key == pygame.K_p:  
                paused = not paused        

    if not paused: 
        
        if boss is None and random.random() < 0.001:  # 0.1% chance to spawn a new boss each frame
            boss = {'shape': 'square', 'color': (255, 255, 0), 'rect': pygame.Rect(random.randint(0, screen_width), 0, 40, 40), 'velocity': 1, 'visible': True, 'boss': True, 'health': 10}
        
        if len(killer_enemies) < min(score // 50, 6) and random.random() < 0.01:  # 1% chance to spawn a new killer enemy each frame
            new_killer_enemy = {'shape': 'circle', 'color': WHITE, 'rect': pygame.Rect(random.randint(0, screen_width), 0, 20, 20), 'velocity': 1, 'visible': True}
            killer_enemies.append(new_killer_enemy)

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
            gun_x = max(gun_x - 5, 0)  # move the gun to the left, but not beyond the left edge of the screen
        if keys[pygame.K_RIGHT]:
            gun_x = min(gun_x + 5, screen_width - gun_width)  # move the gun to the right, but not beyond the right edge of the screen

        screen.fill((0, 0, 0))  

        gun_surface = pygame.Surface((gun_width, gun_height), pygame.SRCALPHA)
        gun_rect = pygame.Rect(0, 0, gun_width, gun_height)
        pygame.draw.rect(gun_surface, WHITE, gun_rect)
        rotated_gun = pygame.transform.rotate(gun_surface, gun_angle)
        rotated_rect = rotated_gun.get_rect(center=(gun_x, gun_y))  # update the gun position
        
        screen.blit(rotated_gun, rotated_rect)

        for bullet in bullets[:]:
            bullet_text = font.render(bullet[2], True, WHITE)  # Render the bullet's character
            screen.blit(bullet_text, (bullet[0].x, bullet[0].y))  # Draw the bullet's character
            for enemy in enemies:
                if bullet[0].colliderect(enemy['rect']) and enemy['visible']:
                    bullets.remove(bullet)
                    enemy['visible'] = False
                    score += 1
                    break
            if boss is not None and bullet[0].colliderect(boss['rect']) and boss['visible']:
                bullets.remove(bullet)
                boss['health'] -= 1  # decrease the boss health
                if boss is not None and 'health' in boss and boss['health'] <= 0:  # if the boss health is 0 or less
                    boss['visible'] = False  # set the boss to not visible
                    score += 10
                    multishot = True
                    multishot_start_time = pygame.time.get_ticks()

        for bullet in bullets:
            bullet[0].x += bullet[1][0] * 5  # Move the bullet in the x direction
            bullet[0].y += bullet[1][1] * 5  # Move the bullet in the y direction

        if boss is not None and boss['visible']:
                    pygame.draw.rect(screen, boss['color'], boss['rect'], 2)
                    boss['rect'].y += boss['velocity']
        else:
            boss = None  # reset the boss when it's not visible

        if boss is None and random.random() < 0.001:  # 0.1% chance to spawn a new boss each frame
            boss = {'shape': 'square', 'color': (255, 255, 0), 'rect': pygame.Rect(random.randint(0, screen_width), 0, 40, 40), 'velocity': 1, 'visible': True, 'boss': True, 'health': 10}

        if multishot and pygame.time.get_ticks() - multishot_start_time > 5000:  # 5 seconds have passed
            multishot = False                

        for killer_enemy in killer_enemies[:]:
            if killer_enemy['visible']:
                pygame.draw.circle(screen, WHITE, killer_enemy['rect'].center, killer_enemy['rect'].width // 2)
                killer_enemy['rect'].y += killer_enemy['velocity']
            if killer_enemy['rect'].colliderect(rotated_rect):  # if the killer enemy collides with the gun
                running = False  # end the game
            elif killer_enemy['rect'].y > screen_height:  # if the killer enemy goes off the screen
                killer_enemies.remove(killer_enemy)  # remove the killer enemy
        
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
               
    else:
        paused_text = paused_font.render('PAUSED', True, WHITE)
        screen.blit(paused_text, (screen_width // 2 - paused_text.get_width() // 2, screen_height // 2 - paused_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()