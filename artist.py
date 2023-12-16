import pygame
import sys


pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


WHITE = (255, 255, 255)


gun_width, gun_height = 20, 60
gun_x, gun_y = screen_width // 2 - gun_width // 2, screen_height - 100  
gun_angle = 0  


bullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                new_bullet = pygame.Rect(gun_x + gun_width // 2 - 2, gun_y - 5, 5, 5)  
                bullets.append(new_bullet)

    
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
    rotated_rect = rotated_gun.get_rect(center=(gun_x + gun_width // 2, gun_y + gun_height // 2))

    
    screen.blit(rotated_gun, rotated_rect)

    
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
        bullet.y -= 5  
        

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
