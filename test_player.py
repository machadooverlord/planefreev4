"""
Teste temporário do Player + Projéteis
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.systems.object_pool import ObjectPool


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Player + Projectiles")
    clock = pygame.time.Clock()
    
    # Criar player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    # Criar pool de projéteis
    projectile_pool = ObjectPool(Projectile, initial_size=50)
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_h:
                    config.show_hitboxes = not config.show_hitboxes
        
        # Input
        keys = pygame.key.get_pressed()
        
        # Update
        player.update(dt, keys)
        
        # Tiro automático
        player.create_projectile(projectile_pool)
        
        # Update projéteis
        projectile_pool.update_all(dt)
        
        # Render
        screen.fill(COLOR_BLACK)
        
        # Renderizar projéteis
        projectile_pool.render_all(screen)
        
        # Renderizar player
        player.render(screen)
        
        # Info
        font = pygame.font.Font(None, 24)
        info = [
            f"Pos: ({int(player.x)}, {int(player.y)})",
            f"HP: {player.hp}/{player.max_hp}",
            f"Projéteis ativos: {projectile_pool.get_active_count()}",
            f"Projéteis disponíveis: {projectile_pool.get_available_count()}",
            f"FPS: {int(clock.get_fps())}",
            f"",
            "WASD/Setas: Mover",
            "Tiro: Automático",
            "H: Toggle Hitbox",
            "ESC: Sair"
        ]
        
        y_offset = 10
        for line in info:
            text = font.render(line, True, COLOR_WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()