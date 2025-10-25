"""
Teste do Kamikaze com diferentes níveis de IA
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player
from src.entities.enemy_kamikaze import EnemyKamikaze


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Kamikaze AI Levels")
    clock = pygame.time.Clock()
    
    # Player (para testar tracking)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    # Criar Kamikazes com diferentes AI levels
    kamikazes = []
    
    # AI Level 0 (esquerda)
    for i in range(3):
        k = EnemyKamikaze()
        k.set_ai_level(0)
        k.spawn(200, -50 - i * 100)
        kamikazes.append(k)
    
    # AI Level 1 (centro)
    for i in range(3):
        k = EnemyKamikaze()
        k.set_ai_level(1)
        k.spawn(SCREEN_WIDTH // 2, -50 - i * 100)
        kamikazes.append(k)
    
    # AI Level 2 (direita)
    for i in range(3):
        k = EnemyKamikaze()
        k.set_ai_level(2)
        k.spawn(SCREEN_WIDTH - 200, -50 - i * 100)
        kamikazes.append(k)
    
    running = True
    spawn_timer = 0
    spawn_interval = 2.0  # Spawna novo a cada 2s
    
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
                
                # 1/2/3 para spawnar com AI level específico
                if event.key == pygame.K_1:
                    k = EnemyKamikaze()
                    k.set_ai_level(0)
                    k.spawn(200, -50)
                    kamikazes.append(k)
                    print("Spawnado: AI Level 0 (Linear)")
                
                if event.key == pygame.K_2:
                    k = EnemyKamikaze()
                    k.set_ai_level(1)
                    k.spawn(SCREEN_WIDTH // 2, -50)
                    kamikazes.append(k)
                    print("Spawnado: AI Level 1 (Tracking)")
                
                if event.key == pygame.K_3:
                    k = EnemyKamikaze()
                    k.set_ai_level(2)
                    k.spawn(SCREEN_WIDTH - 200, -50)
                    kamikazes.append(k)
                    print("Spawnado: AI Level 2 (Zigzag)")
                
                # K para matar todos
                if event.key == pygame.K_k:
                    for k in kamikazes:
                        if k.active:
                            k.take_damage(999)
        
        # Input do player
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y = 1
        
        # Update
        player.update(dt, move_x, move_y)
        
        player_pos = (player.x, player.y)
        for kamikaze in kamikazes:
            kamikaze.update(dt, player_pos)
        
        # Auto-spawn
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            # Spawna um de cada tipo
            import random
            ai_level = random.choice([0, 1, 2])
            x_pos = random.randint(100, SCREEN_WIDTH - 100)
            k = EnemyKamikaze()
            k.set_ai_level(ai_level)
            k.spawn(x_pos, -50)
            kamikazes.append(k)
        
        # Render
        screen.fill(COLOR_BLACK)
        
        # Renderizar kamikazes
        for kamikaze in kamikazes:
            kamikaze.render(screen)
        
        # Renderizar player
        player.render(screen)
        
        # Info
        font = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 18)
        active_count = sum(1 for k in kamikazes if k.active)
        
        info = [
            f"Kamikazes ativos: {active_count}",
            f"FPS: {int(clock.get_fps())}",
            "",
            "WASD: Mover player",
            "1: Spawn AI Lv0 (Linear)",
            "2: Spawn AI Lv1 (Tracking)",
            "3: Spawn AI Lv2 (Zigzag)",
            "K: Matar todos",
            "H: Toggle Hitbox",
            "ESC: Sair",
            "",
            "Auto-spawn: A cada 2s"
        ]
        
        y_offset = 10
        for line in info:
            text = font.render(line, True, COLOR_WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # Labels das colunas
        labels = [
            ("AI Lv0", 200, 50, COLOR_GRAY),
            ("AI Lv1", SCREEN_WIDTH // 2, 50, COLOR_GRAY),
            ("AI Lv2", SCREEN_WIDTH - 200, 50, COLOR_GRAY),
        ]
        
        for text_str, x, y, color in labels:
            text = font_small.render(text_str, True, color)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()