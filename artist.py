import pygame
import sys
import math
import random

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

try:
    pygame.mixer.init()
    bgm = pygame.mixer.Sound('bgm.mp3')
    bgm.play(loops=-1)
    bgm.set_volume(0.5)
    mixer_initialized = True
except pygame.error as e:
    print("An error occurred with the pygame mixer. Details:", e)
    mixer_initialized = False

def play_bgm():
    if mixer_initialized:
        bgm.play(loops=-1)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
NAVY_BLUE = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)


gun_width, gun_height = 20, 60
gun_x, gun_y = screen_width // 2, screen_height - gun_height // 2
gun_angle = 0  

bullets = []
enemies = []
killer_enemies = []

enemy_shapes = ['square', 'triangle', 'circle', 'pentagon']
enemy_colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, MAGENTA, LIME, PINK, BROWN, NAVY_BLUE, LIGHT_BLUE]

boss = None
multishot = False
multishot_start_time = 0

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

paused = False
paused_font = pygame.font.Font(None, 72)  

score = 0
font = pygame.font.Font(None, 36)

boss_colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, MAGENTA, LIME, PINK, BROWN, NAVY_BLUE, LIGHT_BLUE]
boss_sizes = [100, 150, 200]
boss_healths = [10, 15, 20]
boss_velocities = [1]
boss_shapes = ['square', 'circle', 'triangle', 'pentagon']


def spawn_boss():
    return {
        'shape': random.choice(boss_shapes),
        'rect': pygame.Rect(random.randint(0, screen_width - random.choice(boss_sizes)), -random.choice(boss_sizes), random.choice(boss_sizes), random.choice(boss_sizes)),
        'color': random.choice(boss_colors),
        'visible': True,
        'health': random.choice(boss_healths),
        'velocity': random.choice(boss_velocities)
    }

def create_bullet(angle, offset=0):
    bullet_dx = math.sin(math.radians(-angle + offset))
    bullet_dy = -math.cos(math.radians(-angle + offset))
    bullet_x = gun_x + (gun_height // 2) * bullet_dx
    bullet_y = gun_y + (gun_height // 2) * bullet_dy
    bullet_char = random.choice(alphabet)
    return pygame.Rect(bullet_x, bullet_y, 5, 5), (bullet_dx, bullet_dy), bullet_char

def move_and_remove_offscreen_bullets():
    for bullet in bullets[:]:
        bullet[0].x += bullet[1][0] * 5
        bullet[0].y += bullet[1][1] * 5
        if bullet[0].y > screen_height or bullet[0].y < 0:
            bullets.remove(bullet)

def remove_offscreen_enemies(enemy_list):
    for enemy in enemy_list[:]:
        if enemy['rect'].y > screen_height:
            enemy_list.remove(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               bullets.append(create_bullet(gun_angle))
            if multishot:
               bullets.append(create_bullet(gun_angle, -10))
               bullets.append(create_bullet(gun_angle, 10))
            elif event.key == pygame.K_p:  
                paused = not paused
                if 'mixer_initialized' in globals():
                    if paused and mixer_initialized:
                        pygame.mixer.music.pause()  
                    elif mixer_initialized:
                        pygame.mixer.music.unpause()      

    if not paused:
        
        if boss is None and random.random() < 0.001:  
            boss = spawn_boss()
        
        if len(killer_enemies) < min(score // 30, 6) and random.random() < 0.01:  # 1% chance to spawn a new killer enemy each frame
            new_killer_enemy = {'shape': 'circle', 'color': WHITE, 'rect': pygame.Rect(random.randint(0, screen_width), 0, 20, 20), 'velocity': 1, 'visible': True}
            killer_enemies.append(new_killer_enemy)

        if random.random() < 0.02:  # 2% chance to spawn a new enemy each frame
            enemy_shape = random.choice(enemy_shapes)
            enemy_color = random.choice(enemy_colors)
            enemy_x = random.randint(0, screen_width)
            enemy_y = 0
            enemy_velocity = random.randint(1, 3)
            new_enemy = {'shape': enemy_shape, 'color': enemy_color, 'rect': pygame.Rect(enemy_x, enemy_y, 20, 20), 'velocity': enemy_velocity, 'visible': True}
            enemies.append(new_enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            gun_x = max(gun_x - 5, 0)  
        if keys[pygame.K_RIGHT]:
            gun_x = min(gun_x + 5, screen_width - gun_width) 

        screen.fill((0, 0, 0))  

        gun_surface = pygame.Surface((gun_width, gun_height), pygame.SRCALPHA)
        gun_rect = pygame.Rect(0, 0, gun_width, gun_height)
        pygame.draw.rect(gun_surface, WHITE, gun_rect)
        rotated_gun = pygame.transform.rotate(gun_surface, gun_angle)
        rotated_rect = rotated_gun.get_rect(center=(gun_x, gun_y))  
        
        screen.blit(rotated_gun, rotated_rect)
        
        bullets_to_remove = []
        for bullet in bullets[:]:
            bullet_text = font.render(bullet[2], True, WHITE)  
            screen.blit(bullet_text, (bullet[0].x, bullet[0].y))  
            for enemy in enemies:
                if bullet[0].colliderect(enemy['rect']) and enemy['visible']:
                     bullets_to_remove.append(bullet)
                     enemy['visible'] = False
                     score += 1
                     break
                if boss is not None and boss['visible'] and bullet[0].colliderect(boss['rect']):
                    bullets_to_remove.append(bullet)
                    boss['health'] = max(0, boss['health'] - 1)
                    if boss['health'] <= 0: 
                        boss['visible'] = False 
                        score += 10
                        multishot = True
                        multishot_start_time = pygame.time.get_ticks()
                    multishot_start_time = pygame.time.get_ticks()

        for bullet in bullets:
            bullet[0].x += bullet[1][0] * 5  
            bullet[0].y += bullet[1][1] * 5 
                 
        for bullet in bullets[:]:  
            if bullet[0].y > screen_height or bullet[0].y < 0:  
               bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            if bullet in bullets:
               bullets.remove(bullet)       

        for enemy in enemies[:]:  
            if enemy['rect'].y > screen_height:  
                    enemies.remove(enemy)  
           
        for killer_enemy in killer_enemies[:]:  
            if killer_enemy['rect'].y > screen_height:  
                    killer_enemies.remove(killer_enemy) 

        if boss is not None and boss['visible']:
            if boss['shape'] == 'square':
                pygame.draw.rect(screen, boss['color'], boss['rect'], 2)
            elif boss['shape'] == 'circle':
                pygame.draw.ellipse(screen, boss['color'], boss['rect'], 2)
            elif boss['shape'] == 'triangle':
                pygame.draw.polygon(screen, boss['color'], [(boss['rect'].x, boss['rect'].y + boss['rect'].height), (boss['rect'].x + boss['rect'].width // 2, boss['rect'].y), (boss['rect'].x + boss['rect'].width, boss['rect'].y + boss['rect'].height)], 2)
            elif boss['shape'] == 'pentagon':
                pygame.draw.polygon(screen, boss['color'], [(boss['rect'].x + boss['rect'].width // 2, boss['rect'].y), (boss['rect'].x + boss['rect'].width, boss['rect'].y + boss['rect'].height // 3), (boss['rect'].x + 2 * boss['rect'].width // 3, boss['rect'].y + boss['rect'].height), (boss['rect'].x + boss['rect'].width // 3, boss['rect'].y + boss['rect'].height), (boss['rect'].x, boss['rect'].y + boss['rect'].height // 3)], 2)
            boss['rect'].y += boss['velocity']
        else:
            boss = None  

        if multishot and pygame.time.get_ticks() - multishot_start_time > 5000:  
            multishot = False                

        for killer_enemy in killer_enemies[:]:
            if killer_enemy['visible']:
                pygame.draw.circle(screen, WHITE, killer_enemy['rect'].center, killer_enemy['rect'].width // 2)
                killer_enemy['rect'].y += killer_enemy['velocity']
            if killer_enemy['rect'].colliderect(rotated_rect):  
                running = False  
            elif killer_enemy['rect'].y > screen_height:  
                killer_enemies.remove(killer_enemy)     
        
        for enemy in enemies:
            if enemy['visible']:
                if enemy['shape'] == 'square':
                    pygame.draw.rect(screen, enemy['color'], enemy['rect'], 2)
                elif enemy['shape'] == 'triangle':
                    pygame.draw.polygon(screen, enemy['color'], [(enemy['rect'].x, enemy['rect'].y + enemy['rect'].height), (enemy['rect'].x + enemy['rect'].width // 2, enemy['rect'].y), (enemy['rect'].x + enemy['rect'].width, enemy['rect'].y + enemy['rect'].height)], 2)
                elif enemy['shape'] == 'circle':
                    pygame.draw.circle(screen, enemy['color'], enemy['rect'].center, enemy['rect'].width // 2, 2)
                elif enemy['shape'] == 'pentagon':
                    pygame.draw.polygon(screen, enemy['color'], [(enemy['rect'].x + enemy['rect'].width // 2, enemy['rect'].y), (enemy['rect'].x + enemy['rect'].width, enemy['rect'].y + enemy['rect'].height // 3), (enemy['rect'].x + 2 * enemy['rect'].width // 3, enemy['rect'].y + enemy['rect'].height), (enemy['rect'].x + enemy['rect'].width // 3, enemy['rect'].y + enemy['rect'].height), (enemy['rect'].x, enemy['rect'].y + enemy['rect'].height // 3)], 2)
                enemy['rect'].y += enemy['velocity']
            else:
                enemies.remove(enemy)
            if enemy['rect'].colliderect(rotated_rect):
                enemies.remove(enemy)    
                   
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
               
    else:
        paused_text = paused_font.render('PAUSED', True, WHITE)
        screen.blit(paused_text, (screen_width // 2 - paused_text.get_width() // 2, screen_height // 2 - paused_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

