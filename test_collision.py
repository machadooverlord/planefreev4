"""
Teste do Sistema de Colisão
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.entities.enemy_kamikaze import EnemyKamikaze
from src.systems.object_pool import ObjectPool
from src.systems.collision import CollisionSystem


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Collision System")
    clock = pygame.time.Clock()
    
    # Player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    # Projéteis
    projectile_pool = ObjectPool(Projectile, initial_size=50)
    
    # Inimigos
    enemies = []
    
    # Collision system
    collision_system = CollisionSystem()
    
    # Stats
    total_hits = 0
    total_kills = 0
    
    spawn_timer = 0
    spawn_interval = 1.5
    
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
                
                # Spawnar Kamikaze manual
                if event.key == pygame.K_SPACE:
                    k = EnemyKamikaze()
                    k.set_ai_level(1)  # Tracking
                    k.spawn(SCREEN_WIDTH // 2, 100)
                    enemies.append(k)
                    print(f"Kamikaze spawnado! Total: {len(enemies)}")
        
        # Input
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
        
        # Tiro automático
        if player.alive:
            player.create_projectile(projectile_pool)
        
        # Update projéteis
        projectile_pool.update_all(dt)
        
        # Update inimigos
        player_pos = (player.x, player.y)
        for enemy in enemies[:]:
            enemy.update(dt, player_pos)
            if not enemy.active:
                enemies.remove(enemy)
        
        # ===== COLISÕES ===== 
        collision_stats = collision_system.process_collisions(
            player,
            enemies,
            projectile_pool
        )
        
        # Registrar stats
        if collision_stats['player_hit']:
            print(f"⚠️ PLAYER HIT! HP: {player.hp}/{player.max_hp}")
        
        total_hits += collision_stats['enemies_hit']
        
        # Contar kills
        enemies_before = len(enemies)
        enemies = [e for e in enemies if e.active]
        kills = enemies_before - len(enemies)
        total_kills += kills
        
        # Auto-spawn
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            import random
            x = random.randint(200, SCREEN_WIDTH - 200)
            k = EnemyKamikaze()
            k.set_ai_level(random.choice([1, 2]))
            k.spawn(x, -50)
            enemies.append(k)
        
        # Render
        screen.fill(COLOR_BLACK)
        
        # Inimigos
        for enemy in enemies:
            enemy.render(screen)
        
        # Projéteis
        projectile_pool.render_all(screen)
        
        # Player
        player.render(screen)
        
        # HUD
        font = pygame.font.Font(None, 28)
        font_large = pygame.font.Font(None, 48)
        
        # HP grande
        hp_color = COLOR_GREEN if player.hp > 50 else (COLOR_YELLOW if player.hp > 25 else COLOR_RED)
        hp_text = font_large.render(f"HP: {player.hp}/{player.max_hp}", True, hp_color)
        screen.blit(hp_text, (20, 20))
        
        # Stats
        info = [
            f"Inimigos: {len(enemies)}",
            f"Projéteis: {projectile_pool.get_active_count()}",
            f"Total Hits: {total_hits}",
            f"Total Kills: {total_kills}",
            f"FPS: {int(clock.get_fps())}",
            "",
            "WASD: Mover",
            "SPACE: Spawn Kamikaze",
            "H: Toggle Hitbox",
            "ESC: Sair"
        ]
        
        y_offset = 100
        for line in info:
            text = font.render(line, True, COLOR_WHITE)
            screen.blit(text, (20, y_offset))
            y_offset += 30
        
        # Game Over
        if not player.alive:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(COLOR_BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("GAME OVER", True, COLOR_RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)
            
            stats_text = font.render(f"Kills: {total_kills} | Hits: {total_hits}", True, COLOR_WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(stats_text, stats_rect)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()