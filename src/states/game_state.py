"""
GameState - Estado principal de gameplay
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from config import config as game_config
from src.entities.player import Player
from src.entities.projectile import Projectile
from src.systems.object_pool import ObjectPool
from src.core.input_manager import InputManager
from src.background.starfield import Background


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
        self.projectile_pool = ObjectPool(Projectile, initial_size=100)
        
        # Estado
        self.paused = False
        self.game_over = False
        self.current_fps = 0
        
        print("✓ GameState inicializado")
    
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
                
                # Ajustar velocidade do starfield
                if event.key == pygame.K_1:
                    self.background.starfield.set_scroll_speed(0.5)
                    print("Starfield speed: 0.5x")
                if event.key == pygame.K_2:
                    self.background.starfield.set_scroll_speed(1.0)
                    print("Starfield speed: 1.0x")
                if event.key == pygame.K_3:
                    self.background.starfield.set_scroll_speed(2.0)
                    print("Starfield speed: 2.0x")
                if event.key == pygame.K_4:
                    self.background.starfield.set_scroll_speed(3.0)
                    print("Starfield speed: 3.0x (HYPERSPEED!)")
                
                # Ajustar densidade de estrelas
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    new_count = max(50, self.background.starfield.star_count - 50)
                    self.background.starfield.set_density(new_count)
                    print(f"Star density: {new_count}")
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    new_count = min(500, self.background.starfield.star_count + 50)
                    self.background.starfield.set_density(new_count)
                    print(f"Star density: {new_count}")
    
    def update(self, dt, fps=0):
        """
        Atualiza o estado do jogo
        
        Args:
            dt (float): Delta time em segundos
            fps (int): FPS atual
        """
        if self.paused or self.game_over:
            return
        
        # Guardar FPS para renderizar
        self.current_fps = fps
        
        # Update input
        self.input_manager.update()
        
        # Pegar movimento do player
        move_x, move_y = self.input_manager.get_movement(player_index=0)
        
        # Update componentes
        self.background.update(dt)
        self.player.update(dt, move_x, move_y)
        
        # Tiro automático
        if self.player.alive:
            self.player.create_projectile(self.projectile_pool)
        
        # Update projéteis
        self.projectile_pool.update_all(dt)
        
        # Check game over
        if not self.player.alive and not self.game_over:
            self.game_over = True
            print("GAME OVER!")
    
    def render(self):
        """Renderiza o estado do jogo"""
        # Background
        self.background.render(self.screen)
        
        # Projéteis
        self.projectile_pool.render_all(self.screen)
        
        # Player
        self.player.render(self.screen)
        
        # HUD (simples por enquanto)
        self.render_hud()
        
        # Pause overlay
        if self.paused:
            self.render_pause_overlay()
        
        # Game Over overlay
        if self.game_over:
            self.render_game_over_overlay()
    
    def render_hud(self):
        """Renderiza HUD básico"""
        font = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 20)
        
        # HP
        hp_text = font.render(
            f"HP: {self.player.hp}/{self.player.max_hp}",
            True,
            COLOR_GREEN if self.player.hp > 30 else COLOR_RED
        )
        self.screen.blit(hp_text, (20, 20))
        
        # FPS (debug)
        if game_config.show_fps:
            fps = int(self.current_fps)
            fps_text = font.render(f"FPS: {fps}", True, COLOR_WHITE)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 120, 20))
        
        # Info debug
        if game_config.debug_mode:
            info_lines = [
                f"Projéteis: {self.projectile_pool.get_active_count()}",
                f"Estrelas: {self.background.starfield.star_count}",
                f"Star Speed: {self.background.starfield.scroll_speed_multiplier:.1f}x",
            ]
            
            y_offset = 60
            for line in info_lines:
                text = font_small.render(line, True, COLOR_GRAY)
                self.screen.blit(text, (20, y_offset))
                y_offset += 22
    
    def render_pause_overlay(self):
        """Renderiza overlay de pause"""
        # Semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto
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
        # Semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto
        font_large = pygame.font.Font(None, 96)
        font_small = pygame.font.Font(None, 36)
        
        game_over_text = font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        instruction_text = font_small.render("Pressione ESC para sair", True, COLOR_GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instruction_text, instruction_rect)