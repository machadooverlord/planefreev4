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
from src.entities.card import CardManager
from src.entities.card_drop import CardDrop
from src.ui.card_menu import CardMenu


class GameState:
    """Estado de gameplay ativo"""
    
    def __init__(self, screen):
        """Inicializa o estado de jogo"""
        self.screen = screen
        
        # Componentes
        self.background = Background()
        self.input_manager = InputManager()
        
        # Player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        # Projéteis
        self.projectile_pool = ObjectPool(Projectile, initial_size=200)
        
        # Collectibles (minérios)
        from src.entities.collectible import Collectible
        self.collectible_pool = ObjectPool(Collectible, initial_size=100)
        self.player_minerals = 0
        
        # Sistema de colisão
        self.collision_system = CollisionSystem()
        
        # Wave Manager
        self.wave_manager = WaveManager()
        
        # Card Manager
        self.card_manager = CardManager()
        
        # Card Drops (pool)
        self.card_drop_pool = ObjectPool(CardDrop, initial_size=20)
        
        # Card Menu
        self.card_menu = CardMenu()
        
        # ✅ NOVO: Efeito visual de coleta de carta
        self.card_collect_effect = None  # {'timer': float, 'card_name': str, 'rarity': str}
        
        # Estado
        self.paused = False
        self.game_over = False
        self.current_fps = 0
        
        print("✅ GameState inicializado")
    
    def handle_events(self, events):
        """Processa eventos"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Abrir/fechar card menu (TAB)
                if event.key == pygame.K_TAB:
                    if not self.game_over:
                        self.card_menu.toggle()
                        return
                
                # Pausa
                if event.key == pygame.K_PAUSE and not self.card_menu.active:
                    self.paused = not self.paused
                    print(f"Pause: {self.paused}")
                
                # ✅ NOVO: Velocidade do starfield (5% por nível)
                if event.key == pygame.K_1:
                    self.background.starfield.set_scroll_speed(0.95)  # -5%
                    print("⭐ Starfield speed: 0.95x (-5%)")
                if event.key == pygame.K_2:
                    self.background.starfield.set_scroll_speed(1.0)   # Normal
                    print("⭐ Starfield speed: 1.0x (Normal)")
                if event.key == pygame.K_3:
                    self.background.starfield.set_scroll_speed(1.05)  # +5%
                    print("⭐ Starfield speed: 1.05x (+5%)")
                if event.key == pygame.K_4:
                    self.background.starfield.set_scroll_speed(1.10)  # +10%
                    print("⭐ Starfield speed: 1.10x (+10%)")
                if event.key == pygame.K_5:
                    self.background.starfield.set_scroll_speed(1.15)  # +15%
                    print("⭐ Starfield speed: 1.15x (+15%)")
                
                # DENSIDADE DE ESTRELAS
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    new_count = max(50, self.background.starfield.star_count - 50)
                    self.background.starfield.set_density(new_count)
                    print(f"⭐ Star density: {new_count}")
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    new_count = min(500, self.background.starfield.star_count + 50)
                    self.background.starfield.set_density(new_count)
                    print(f"⭐ Star density: {new_count}")
    
    def update(self, dt, fps=0):
        """Atualiza o estado do jogo"""
        # Guardar FPS
        self.current_fps = fps
        
        # Update card menu
        self.card_menu.update(dt, self.input_manager, self.player)
        
        # ✅ NOVO: Update efeito de coleta
        if self.card_collect_effect:
            self.card_collect_effect['timer'] -= dt
            if self.card_collect_effect['timer'] <= 0:
                self.card_collect_effect = None
        
        # Se menu aberto, pausar gameplay
        if self.card_menu.active:
            return
        
        if self.paused or self.game_over:
            return
        
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
            if hasattr(enemy, 'can_spawn_child'):
                if enemy.can_spawn_child():
                    if random.random() < 0.75:
                        child = self.wave_manager.get_kamikaze()
                    else:
                        child = self.wave_manager.get_range()
                    enemy.spawn_child(child)
        
        # Colisões
        collision_stats = self.collision_system.process_collisions(
            self.player,
            active_enemies,
            self.projectile_pool
        )
        
        # DROPAR MINÉRIOS E CARTAS
        enemies_to_deactivate = []
        
        for enemy in active_enemies:
            if not enemy.alive and not enemy.has_dropped:
                # MINÉRIOS
                drop_amount = enemy.value
                
                if enemy.enemy_type == 'kamikaze':
                    num_drops = 1
                elif enemy.enemy_type == 'range':
                    num_drops = 2
                elif enemy.enemy_type == 'mother':
                    num_drops = 5
                else:
                    num_drops = 1
                
                for i in range(num_drops):
                    mineral = self.collectible_pool.get()
                    offset_x = random.randint(-15, 15) * i
                    offset_y = random.randint(-10, 10) * i
                    mineral.spawn(
                        enemy.x + offset_x,
                        enemy.y + offset_y,
                        drop_amount // num_drops
                    )
                
                # ✅ AUMENTADO: Chance de dropar carta (3x mais frequente)
                drop_chance = self._get_card_drop_chance(enemy.enemy_type)
                
                if random.random() < drop_chance:
                    rarity = self.card_manager.roll_rarity()
                    card = self.card_manager.get_random_card(rarity)
                    card_drop = self.card_drop_pool.get()
                    card_drop.spawn(enemy.x, enemy.y, card)
                    print(f"🎴 CARTA DROPADA: {card.name} ({card.rarity})")
                
                enemy.has_dropped = True
                enemies_to_deactivate.append(enemy)
        
        for enemy in enemies_to_deactivate:
            enemy.deactivate()
        
        # Update Wave Manager
        self.wave_manager.update(dt, active_enemies)
        
        # Update collectibles
        self.collectible_pool.update_all(dt)
        
        # Update card drops
        self.card_drop_pool.update_all(dt)
        
        # Coletar minérios
        for collectible in self.collectible_pool.in_use[:]:
            if not collectible.active:
                continue
            
            dx = collectible.x - self.player.x
            dy = collectible.y - self.player.y
            distance_sq = dx*dx + dy*dy
            collect_radius = 30
            
            if distance_sq < collect_radius * collect_radius:
                value = collectible.collect()
                self.player_minerals += value
        
        # Coletar cartas
        for card_drop in self.card_drop_pool.in_use[:]:
            if not card_drop.active:
                continue
            
            dx = card_drop.x - self.player.x
            dy = card_drop.y - self.player.y
            distance_sq = dx*dx + dy*dy
            
            if distance_sq <= card_drop.collect_radius * card_drop.collect_radius:
                collect_pressed = (
                    self.input_manager.is_key_pressed(pygame.K_e) or
                    self.input_manager.get_button('A', 0)
                )
                
                if collect_pressed:
                    if len(self.player.equipped_cards) >= self.player.max_card_slots:
                        print(f"⚠️ Slots cheios! Abra o menu (TAB) para remover uma carta primeiro.")
                    else:
                        # ✅ NOVO: Guardar info da carta antes de coletar
                        card_name = card_drop.card.name
                        card_rarity = card_drop.card.rarity
                        
                        # Coletar
                        collected = card_drop.check_collect_input(self.input_manager, self.player)
                        
                        # Se coletou, ativar efeito visual
                        if collected:
                            self.card_collect_effect = {
                                'timer': 3.0,  # 3 segundos
                                'card_name': card_name,
                                'rarity': card_rarity
                            }
        
        # Check game over
        if not self.player.alive and not self.game_over:
            self.game_over = True
            print("💀 GAME OVER!")
    
    def _get_card_drop_chance(self, enemy_type):
        """
        Calcula chance de dropar carta
        ✅ AUMENTADO: 3x mais frequente
        """
        if enemy_type == 'kamikaze':
            return 0.15  # Era 0.05 → 15%
        elif enemy_type == 'range':
            return 0.30  # Era 0.10 → 30%
        elif enemy_type == 'mother':
            return 0.70  # Era 0.35 → 70%
        else:
            return 0.15
    
    def render(self):
        """Renderiza o estado do jogo"""
        # Background
        self.background.render(self.screen)
        
        # Inimigos
        for enemy in self.wave_manager.get_active_enemies():
            enemy.render(self.screen)
            
            if hasattr(enemy, 'children'):
                for child in enemy.children:
                    if child.active:
                        child.render(self.screen)
        
        # Collectibles
        self.collectible_pool.render_all(self.screen)
        
        # Card drops
        self.card_drop_pool.render_all(self.screen)
        
        # Card collect prompts
        for card_drop in self.card_drop_pool.in_use:
            if card_drop.active:
                card_drop.render_collect_prompt(self.screen, self.player)
        
        # Projéteis
        self.projectile_pool.render_all(self.screen)
        
        # Player
        self.player.render(self.screen)
        
        # HUD
        self.render_hud()
        
        # ✅ NOVO: Efeito de coleta de carta
        if self.card_collect_effect:
            self.render_card_collect_effect()
        
        # Countdown
        self.render_countdown()
        
        # Card Menu
        self.card_menu.render(self.screen, self.player)
        
        # Pause
        if self.paused and not self.card_menu.active:
            self.render_pause_overlay()
        
        # Game Over
        if self.game_over:
            self.render_game_over_overlay()
    
    def render_card_collect_effect(self):
        """✅ NOVO: Renderiza efeito visual ao coletar carta"""
        if not self.card_collect_effect:
            return
        
        # Informações
        card_name = self.card_collect_effect['card_name']
        card_rarity = self.card_collect_effect['rarity']
        timer = self.card_collect_effect['timer']
        
        # Cor baseada na raridade
        if card_rarity == 'comum':
            color = (200, 200, 200)
        elif card_rarity == 'incomum':
            color = (100, 150, 255)
        elif card_rarity == 'epico':
            color = (200, 0, 255)
        else:
            color = (255, 255, 255)
        
        # Fade out nos últimos 0.5s
        alpha = 255
        if timer < 0.5:
            alpha = int((timer / 0.5) * 255)
        
        # Posição (topo da tela, centralizado)
        y_pos = 150 + int((3.0 - timer) * 20)  # Desce suavemente
        
        # Fontes
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        
        # Texto "NOVA CARTA!"
        new_card_text = font_large.render("NOVA CARTA!", True, color)
        new_card_rect = new_card_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        
        # Texto do nome da carta
        name_text = font_medium.render(card_name, True, color)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 50))
        
        # Texto da raridade
        rarity_text = font_medium.render(card_rarity.upper(), True, color)
        rarity_rect = rarity_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 85))
        
        # Aplicar alpha
        new_card_text.set_alpha(alpha)
        name_text.set_alpha(alpha)
        rarity_text.set_alpha(alpha)
        
        # Fundo semi-transparente
        bg_width = 500
        bg_height = 140
        bg_x = (SCREEN_WIDTH - bg_width) // 2
        bg_y = y_pos - 40
        
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, int(200 * (alpha / 255))))
        
        # Borda colorida
        border_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, (*color, alpha), (0, 0, bg_width, bg_height), 4)
        
        # Blit
        self.screen.blit(bg_surface, (bg_x, bg_y))
        self.screen.blit(border_surface, (bg_x, bg_y))
        self.screen.blit(new_card_text, new_card_rect)
        self.screen.blit(name_text, name_rect)
        self.screen.blit(rarity_text, rarity_rect)
    
    def render_hud(self):
        """Renderiza HUD"""
        font = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        # HP
        hp_text = font.render(
            f"HP: {int(self.player.hp)}/{self.player.max_hp}",
            True,
            COLOR_GREEN if self.player.hp > 30 else COLOR_RED
        )
        self.screen.blit(hp_text, (20, 20))
        
        # Minérios
        mineral_text = font.render(
            f"MINERIOS: {self.player_minerals}",
            True,
            COLOR_YELLOW
        )
        self.screen.blit(mineral_text, (20, 60))
        
        # Cartas equipadas
        cards_equipped = len(self.player.equipped_cards)
        cards_text = font.render(
            f"CARTAS: {cards_equipped}/{self.player.max_card_slots}",
            True,
            COLOR_CYAN
        )
        self.screen.blit(cards_text, (20, 100))
        
        # Hint de menu
        hint_text = font_small.render("[TAB] Menu de Cartas", True, COLOR_GRAY)
        self.screen.blit(hint_text, (20, 135))
        
        # Setor
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
                f"Pierce: {self.player.pierce}",
                f"Spawned: {self.wave_manager.enemies_spawned}/{self.wave_manager.enemies_to_spawn}",
            ]
            
            y_offset = 170
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
                
                text1 = font_large.render(lines[0], True, (0, 255, 255))
                rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
                
                text2 = font_huge.render(lines[1], True, COLOR_YELLOW)
                rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                
                shadow1 = font_large.render(lines[0], True, COLOR_BLACK)
                shadow_rect1 = shadow1.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 57))
                shadow2 = font_huge.render(lines[1], True, COLOR_BLACK)
                shadow_rect2 = shadow2.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 + 44))
                
                self.screen.blit(shadow1, shadow_rect1)
                self.screen.blit(shadow2, shadow_rect2)
                self.screen.blit(text1, rect1)
                self.screen.blit(text2, rect2)
            else:
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
        
        instruction_text = font_small.render("Pressione PAUSE para continuar", True, COLOR_GRAY)
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
        
        game_over_text = font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        stats_text = font_medium.render(
            f"SETOR {self.wave_manager.current_sector}",
            True,
            COLOR_WHITE
        )
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(stats_text, stats_rect)
        
        minerals_text = font_small.render(
            f"MINERIOS: {self.player_minerals}",
            True,
            COLOR_YELLOW
        )
        minerals_rect = minerals_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(minerals_text, minerals_rect)
        
        instruction_text = font_small.render("Pressione ESC para sair", True, COLOR_GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(instruction_text, instruction_rect)