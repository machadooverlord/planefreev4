"""
GameState - Estado principal de gameplay
"""

import pygame
import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from config import config as game_config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.systems.object_pool import ObjectPool
from src.core.input_manager import InputManager
from src.background.starfield import Background
from src.systems.collision import CollisionSystem
from src.systems.wave_manager import WaveManager


class GameState:
    """Estado de gameplay ativo"""
    
    def __init__(self, screen):
        """
        Inicializa o estado de jogo
        
        Args:
            screen: Pygame surface
        """
        self.screen = screen
        
        # Componentes
        self.background = Background()
        self.input_manager = InputManager()
        
        # Player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        # Projéteis
        self.projectile_pool = ObjectPool(Projectile, initial_size=200)
        
        # ✅ NOVO: Collectibles (minérios)
        from src.entities.collectible import Collectible
        self.collectible_pool = ObjectPool(Collectible, initial_size=100)
        self.player_minerals = 0
        
        # Sistema de colisão
        self.collision_system = CollisionSystem()
        
        # ✅ Wave Manager (já inicia automaticamente)
        self.wave_manager = WaveManager()
        
        # Estado
        self.paused = False
        self.game_over = False
        self.current_fps = 0
        
        print("✅ GameState inicializado")
    
    def handle_events(self, events):
        """
        Processa eventos
        
        Args:
            events: Lista de eventos do Pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Pausa
                if event.key == pygame.K_TAB or event.key == pygame.K_PAUSE:
                    self.paused = not self.paused
                    print(f"Pause: {self.paused}")
                
                # ✅ CONTROLES DE VELOCIDADE DO STARFIELD
                if event.key == pygame.K_1:
                    self.background.starfield.set_scroll_speed(0.5)
                    print("⭐ Starfield speed: 0.5x")
                if event.key == pygame.K_2:
                    self.background.starfield.set_scroll_speed(1.0)
                    print("⭐ Starfield speed: 1.0x")
                if event.key == pygame.K_3:
                    self.background.starfield.set_scroll_speed(2.0)
                    print("⭐ Starfield speed: 2.0x")
                if event.key == pygame.K_4:
                    self.background.starfield.set_scroll_speed(5.0)
                    print("⭐ Starfield speed: 5.0x (TESTE RÁPIDO)")
                
                # ✅ DENSIDADE DE ESTRELAS
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    new_count = max(50, self.background.starfield.star_count - 50)
                    self.background.starfield.set_density(new_count)
                    print(f"⭐ Star density: {new_count}")
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    new_count = min(500, self.background.starfield.star_count + 50)
                    self.background.starfield.set_density(new_count)
                    print(f"⭐ Star density: {new_count}")
    
    def update(self, dt, fps=0):
        """
        Atualiza o estado do jogo
        
        Args:
            dt (float): Delta time em segundos
            fps (int): FPS atual
        """
        if self.paused or self.game_over:
            return
        
        # Guardar FPS
        self.current_fps = fps
        
        # Update input
        self.input_manager.update()
        
        # Movimento do player
        move_x, move_y = self.input_manager.get_movement(player_index=0)
        
        # Update componentes
        self.background.update(dt)
        self.player.update(dt, move_x, move_y)
        
        # Tiro automático
        if self.player.alive:
            self.player.create_projectile(self.projectile_pool)
        
        # Update projéteis
        self.projectile_pool.update_all(dt)
        
        # Pegar inimigos ativos
        active_enemies = self.wave_manager.get_active_enemies()
        
        # Update inimigos
        player_pos = (self.player.x, self.player.y) if self.player.alive else None
        for enemy in active_enemies:
            enemy.update(dt, player_pos)
            
            # Ranges atiram
            if hasattr(enemy, 'can_fire') and enemy.can_fire():
                enemy.shoot(self.projectile_pool, player_pos)
            
            # Mães spawnam filhotes
            for enemy in active_enemies:
                if hasattr(enemy, 'can_spawn_child'):
                    if enemy.can_spawn_child():
                        # 75% Kamikaze, 25% Range
                        if random.random() < 0.75:
                            child = self.wave_manager.get_kamikaze()
                            print(f"🎲 Escolheu Kamikaze para filhote")
                        else:
                            child = self.wave_manager.get_range()
                            print(f"🎲 Escolheu Range para filhote")
                        
                        success = enemy.spawn_child(child)
                        if success:
                            print(f"✅ Filhote spawnado com sucesso!")
        
        # Colisões
        collision_stats = self.collision_system.process_collisions(
            self.player,
            active_enemies,
            self.projectile_pool
        )
        
        # ✅ DROPAR MINÉRIOS (sem desativar ainda)
        enemies_to_deactivate = []
        
        for enemy in active_enemies:
            if not enemy.alive and not enemy.has_dropped:
                # Quantidade baseada no tipo
                drop_amount = enemy.value
                
                # Dropar MÚLTIPLOS minérios
                if enemy.enemy_type == 'kamikaze':
                    num_drops = 1
                elif enemy.enemy_type == 'range':
                    num_drops = 2
                elif enemy.enemy_type == 'mother':
                    num_drops = 5
                else:
                    num_drops = 1
                
                # Dropar os minérios
                for i in range(num_drops):
                    mineral = self.collectible_pool.get()
                    offset_x = random.randint(-15, 15) * i
                    offset_y = random.randint(-10, 10) * i
                    mineral.spawn(
                        enemy.x + offset_x,
                        enemy.y + offset_y,
                        drop_amount // num_drops
                    )
                
                enemy.has_dropped = True
                enemies_to_deactivate.append(enemy)
                
                print(f"💎 DROP: {num_drops}x minérios de {enemy.enemy_type}")
        
        # ✅ Desativar APÓS o loop
        for enemy in enemies_to_deactivate:
            enemy.deactivate()
        
        # Update Wave Manager
        self.wave_manager.update(dt, active_enemies)
        
        # Update collectibles
        self.collectible_pool.update_all(dt)
        
        # Coletar minérios
        for collectible in self.collectible_pool.in_use[:]:
            if not collectible.active:
                continue
            
            # Colisão com player
            dx = collectible.x - self.player.x
            dy = collectible.y - self.player.y
            distance_sq = dx*dx + dy*dy
            collect_radius = 30
            
            if distance_sq < collect_radius * collect_radius:
                value = collectible.collect()
                self.player_minerals += value
                print(f"✅ COLETOU {value}! Total: {self.player_minerals}")
        
        # Check game over
        if not self.player.alive and not self.game_over:
            self.game_over = True
            print("💀 GAME OVER!")
    
    def render(self):
        """Renderiza o estado do jogo"""
        # Background
        self.background.render(self.screen)
        
        # Inimigos (incluindo filhotes)
        for enemy in self.wave_manager.get_active_enemies():
            enemy.render(self.screen)
            
            # ✅ Renderizar filhotes da mãe
            if hasattr(enemy, 'children'):
                for child in enemy.children:
                    if child.active:
                        child.render(self.screen)
        
        # Collectibles
        self.collectible_pool.render_all(self.screen)
        
        # Projéteis
        self.projectile_pool.render_all(self.screen)
        
        # Player
        self.player.render(self.screen)
        
        # HUD
        self.render_hud()
        
        # Countdown
        self.render_countdown()
        
        # Pause
        if self.paused:
            self.render_pause_overlay()
        
        # Game Over
        if self.game_over:
            self.render_game_over_overlay()
    
    def render_hud(self):
        """Renderiza HUD"""
        font = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        # HP
        hp_text = font.render(
            f"HP: {self.player.hp}/{self.player.max_hp}",
            True,
            COLOR_GREEN if self.player.hp > 30 else COLOR_RED
        )
        self.screen.blit(hp_text, (20, 20))
        
        # ✅ Minérios
        mineral_text = font.render(
            f"MINERIOS: {self.player_minerals}",
            True,
            COLOR_YELLOW
        )
        self.screen.blit(mineral_text, (20, 60))
        
        # ✅ CORRETO: Setor (sem wave)
        sector_text = font.render(
            f"SETOR {self.wave_manager.current_sector}",
            True,
            COLOR_WHITE
        )
        sector_rect = sector_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(sector_text, sector_rect)
        
        # FPS
        if game_config.show_fps:
            fps_text = font_small.render(f"FPS: {int(self.current_fps)}", True, COLOR_WHITE)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 20))
        
        # Debug info
        if game_config.debug_mode:
            active_enemies = self.wave_manager.get_active_enemies()
            info_lines = [
                f"Inimigos: {len(active_enemies)}",
                f"Projéteis: {self.projectile_pool.get_active_count()}",
                f"Minérios: {self.collectible_pool.get_active_count()}",
                f"Spawned: {self.wave_manager.enemies_spawned}/{self.wave_manager.enemies_to_spawn}",
            ]
            
            y_offset = 100
            for line in info_lines:
                text = font_small.render(line, True, COLOR_GRAY)
                self.screen.blit(text, (20, y_offset))
                y_offset += 25
    
    def render_countdown(self):
        """Renderiza countdown entre SETORES"""
        countdown_text = self.wave_manager.get_countdown_text()
        
        if countdown_text:
            font_huge = pygame.font.Font(None, 120)
            font_large = pygame.font.Font(None, 80)
            
            if '\n' in countdown_text:
                lines = countdown_text.split('\n')
                
                # Linha 1: SETOR X
                text1 = font_large.render(lines[0], True, (0, 255, 255))  # ✅ Cyan direto
                rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
                
                # Linha 2: Número
                text2 = font_huge.render(lines[1], True, COLOR_YELLOW)
                rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                
                # Sombras
                shadow1 = font_large.render(lines[0], True, COLOR_BLACK)
                shadow_rect1 = shadow1.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 57))
                shadow2 = font_huge.render(lines[1], True, COLOR_BLACK)
                shadow_rect2 = shadow2.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 44))
                
                self.screen.blit(shadow1, shadow_rect1)
                self.screen.blit(shadow2, shadow_rect2)
                self.screen.blit(text1, rect1)
                self.screen.blit(text2, rect2)
            
            else:
                # "GO!"
                text = font_huge.render(countdown_text, True, COLOR_GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                
                shadow = font_huge.render(countdown_text, True, COLOR_BLACK)
                shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 4))
                
                self.screen.blit(shadow, shadow_rect)
                self.screen.blit(text, text_rect)
        
    def render_pause_overlay(self):
        """Renderiza overlay de pause"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        pause_text = font_large.render("PAUSADO", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        instruction_text = font_small.render("Pressione TAB para continuar", True, COLOR_GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instruction_text, instruction_rect)
    
    def render_game_over_overlay(self):
        """Renderiza overlay de game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # GAME OVER
        game_over_text = font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # ✅ Stats (sem wave)
        stats_text = font_medium.render(
            f"SETOR {self.wave_manager.current_sector}",
            True,
            COLOR_WHITE
        )
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(stats_text, stats_rect)
        
        # ✅ Minérios coletados
        minerals_text = font_small.render(
            f"MINERIOS COLETADOS: {self.player_minerals}",
            True,
            COLOR_YELLOW
        )
        minerals_rect = minerals_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(minerals_text, minerals_rect)
        
        # Instruções
        instruction_text = font_small.render("Pressione ESC para sair", True, COLOR_GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(instruction_text, instruction_rect)