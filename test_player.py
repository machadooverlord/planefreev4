"""
Teste temporário do Player
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Player Movement")
    clock = pygame.time.Clock()
    
    # Criar player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
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
        
        # Render
        screen.fill(COLOR_BLACK)
        player.render(screen)
        
        # Info
        font = pygame.font.Font(None, 24)
        info = [
            f"Pos: ({int(player.x)}, {int(player.y)})",
            f"Vel: ({int(player.vx)}, {int(player.vy)})",
            f"HP: {player.hp}/{player.max_hp}",
            f"FPS: {int(clock.get_fps())}",
            f"",
            "WASD/Setas: Mover",
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