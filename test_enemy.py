"""
Teste temporário da classe Enemy
"""

import pygame
from constants import *
from config import config
from src.entities.enemy import Enemy


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test: Enemy Base")
    clock = pygame.time.Clock()
    
    # Criar alguns inimigos de teste
    enemies = []
    for i in range(5):
        enemy = Enemy(0, 0)
        enemy.spawn(200 + i * 150, -50)
        enemies.append(enemy)
    
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
                
                # D para dar dano em TODOS os inimigos ativos
                if event.key == pygame.K_d:
                    damaged_count = 0
                    for enemy in enemies:
                        if enemy.active and enemy.alive:
                            enemy.take_damage(10)
                            damaged_count += 1
                    if damaged_count > 0:
                        print(f"Dano dado em {damaged_count} inimigos")
                
                # X para dar dano APENAS no primeiro
                if event.key == pygame.K_x:
                    for enemy in enemies:
                        if enemy.active and enemy.alive:
                            enemy.take_damage(10)
                            print(f"Enemy HP: {enemy.hp}/{enemy.max_hp}")
                            break
                
                # S para spawnar novo
                if event.key == pygame.K_s:
                    enemy = Enemy(0, 0)
                    enemy.spawn(400, -50)
                    enemies.append(enemy)
                    print("Novo inimigo spawnado")
                
                # K para matar todos
                if event.key == pygame.K_k:
                    killed = 0
                    for enemy in enemies:
                        if enemy.active and enemy.alive:
                            enemy.take_damage(999)
                            killed += 1
                    print(f"Matou {killed} inimigos")
        
        # Update
        for enemy in enemies:
            enemy.update(dt)
        
        # Render
        screen.fill(COLOR_BLACK)
        
        for enemy in enemies:
            enemy.render(screen)
        
        # Info
        font = pygame.font.Font(None, 24)
        active_count = sum(1 for e in enemies if e.active)
        alive_count = sum(1 for e in enemies if e.alive)
        info = [
            f"Inimigos ativos: {active_count}/{len(enemies)}",
            f"Inimigos vivos: {alive_count}/{len(enemies)}",
            f"FPS: {int(clock.get_fps())}",
            "",
            "H: Toggle Hitbox",
            "D: Dar dano em TODOS (10 HP)",
            "X: Dar dano no primeiro (10 HP)",
            "K: Matar TODOS (999 HP)",
            "S: Spawnar novo inimigo",
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