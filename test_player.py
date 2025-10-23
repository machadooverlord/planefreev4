"""
Teste temporário do Player + Projéteis + Input + Background
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.systems.object_pool import ObjectPool
from src.core.input_manager import InputManager
from src.background.starfield import Background


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Full Core Gameplay")
    clock = pygame.time.Clock()
    
    # Criar background
    background = Background()
    
    # Criar player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    # Criar pool de projéteis
    projectile_pool = ObjectPool(Projectile, initial_size=50)
    
    # Criar input manager
    input_manager = InputManager()
    
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
                # Ajustar velocidade do starfield (teste)
                if event.key == pygame.K_1:
                    background.starfield.set_scroll_speed(0.5)
                if event.key == pygame.K_2:
                    background.starfield.set_scroll_speed(1.0)
                if event.key == pygame.K_3:
                    background.starfield.set_scroll_speed(2.0)
                # Ajustar densidade (teste)
                if event.key == pygame.K_MINUS:
                    background.starfield.set_density(
                        max(50, background.starfield.star_count - 50)
                    )
                if event.key == pygame.K_EQUALS:
                    background.starfield.set_density(
                        min(500, background.starfield.star_count + 50)
                    )
        
        # Update input manager
        input_manager.update()
        
        # Pegar movimento (player 0)
        move_x, move_y = input_manager.get_movement(player_index=0)
        
        # Update
        background.update(dt)
        player.update(dt, move_x, move_y)
        
        # Tiro automático
        player.create_projectile(projectile_pool)
        
        # Update projéteis
        projectile_pool.update_all(dt)
        
        # ===== RENDER =====
        
        # Renderizar background (PRIMEIRO)
        background.render(screen)
        
        # Renderizar projéteis
        projectile_pool.render_all(screen)
        
        # Renderizar player
        player.render(screen)
        
        # Info
        font = pygame.font.Font(None, 24)
        info = [
            f"Pos: ({int(player.x)}, {int(player.y)})",
            f"Input: ({move_x:.2f}, {move_y:.2f})",
            f"HP: {player.hp}/{player.max_hp}",
            f"Projéteis: {projectile_pool.get_active_count()}",
            f"Estrelas: {background.starfield.star_count}",
            f"Star Speed: {background.starfield.scroll_speed_multiplier}x",
            f"Gamepads: {input_manager.get_joystick_count()}",
            f"FPS: {int(clock.get_fps())}",
            f"",
            "WASD/Setas: Mover",
            "1/2/3: Star speed (0.5x/1x/2x)",
            "-/+: Star density",
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