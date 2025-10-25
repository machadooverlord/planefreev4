"""
Teste do Enemy Range (atira de longe)
"""

import pygame
from constants import *
from config import config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.entities.enemy_range import EnemyRange
from src.systems.object_pool import ObjectPool
from src.systems.collision import CollisionSystem


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Enemy Range")
    clock = pygame.time.Clock()
    
    # Player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    # Projéteis (compartilhado entre player e inimigos)
    projectile_pool = ObjectPool(Projectile, initial_size=100)
    
    # Inimigos Range
    enemies = []
    
    # Collision system
    collision_system = CollisionSystem()
    
    # Spawnar alguns Ranges iniciais
    for i in range(3):
        r = EnemyRange()
        r.set_ai_level(0)  # Level 0 primeiro
        r.spawn(300 + i * 400, -50)
        enemies.append(r)
    
    # Stats
    player_hits_taken = 0
    enemies_killed = 0
    
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
                
                # 1/2 para spawnar com AI levels
                if event.key == pygame.K_1:
                    r = EnemyRange()
                    r.set_ai_level(0)
                    r.spawn(SCREEN_WIDTH // 2, -50)
                    enemies.append(r)
                    print("Range spawnado: AI Level 0 (Tiro reto)")
                
                if event.key == pygame.K_2:
                    r = EnemyRange()
                    r.set_ai_level(1)
                    r.spawn(SCREEN_WIDTH // 2, -50)
                    enemies.append(r)
                    print("Range spawnado: AI Level 1 (Mira no player)")
                
                # K para matar todos
                if event.key == pygame.K_k:
                    for e in enemies:
                        e.take_damage(999)
        
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
        
        # Tiro automático do player
        if player.alive:
            player.create_projectile(projectile_pool)
        
        # Update projéteis
        projectile_pool.update_all(dt)
        
        # Update inimigos Range
        player_pos = (player.x, player.y) if player.alive else None
        for enemy in enemies[:]:
            enemy.update(dt, player_pos)
            
            # Inimigos Range atiram
            if enemy.can_fire():
                enemy.shoot(projectile_pool, player_pos)
            
            # Remover inativos
            if not enemy.active:
                enemies.remove(enemy)
        
        # Colisões
        old_hp = player.hp
        collision_stats = collision_system.process_collisions(
            player,
            enemies,
            projectile_pool
        )
        
        # Contar hits no player
        if player.hp < old_hp:
            player_hits_taken += 1
            print(f"⚠️ PLAYER HIT! HP: {player.hp}/{player.max_hp} (Total hits: {player_hits_taken})")
        
        # Contar kills
        for enemy in enemies:
            if not enemy.alive and enemy.active:
                enemies_killed += 1
        
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
        
        # HP
        hp_color = COLOR_GREEN if player.hp > 50 else (COLOR_YELLOW if player.hp > 25 else COLOR_RED)
        hp_text = font_large.render(f"HP: {player.hp}/{player.max_hp}", True, hp_color)
        screen.blit(hp_text, (20, 20))
        
        # Stats
        player_projectiles = sum(1 for p in projectile_pool.in_use if p.owner == 'player')
        enemy_projectiles = sum(1 for p in projectile_pool.in_use if p.owner == 'enemy')
        
        info = [
            f"Ranges: {len(enemies)}",
            f"Projéteis Player: {player_projectiles}",
            f"Projéteis Inimigos: {enemy_projectiles}",
            f"Hits no Player: {player_hits_taken}",
            f"Kills: {enemies_killed}",
            f"FPS: {int(clock.get_fps())}",
            "",
            "WASD: Mover",
            "1: Spawn Range AI Lv0 (reto)",
            "2: Spawn Range AI Lv1 (mira)",
            "K: Matar todos",
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
            
            stats_text = font.render(f"Hits Taken: {player_hits_taken} | Kills: {enemies_killed}", True, COLOR_WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(stats_text, stats_rect)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()