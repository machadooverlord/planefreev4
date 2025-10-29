"""
Enemy - Classe base para inimigos
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.utils.placeholder_generator import create_enemy_sprite


class Enemy:
    """Classe base para todos os inimigos"""
    
    def __init__(self, x, y, enemy_type='kamikaze'):
        """
        Inicializa o inimigo
        
        Args:
            x (float): Posição X inicial
            y (float): Posição Y inicial
            enemy_type (str): Tipo do inimigo ('kamikaze', 'range', 'mother')
        """
        # Posição
        self.x = x
        self.y = y
        
        # Tipo
        self.enemy_type = enemy_type
        
        # Stats base (serão sobrescritos pelas subclasses)
        self.max_hp = 30
        self.hp = 30
        self.speed = 100
        self.damage = 20
        self.value = 10  # Minérios que dropa
        
        # Movimento
        self.vx = 0
        self.vy = self.speed  # Para baixo por padrão
        
        # Sprite
        self.size = 24
        self.sprite = create_enemy_sprite(self.size)
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Hitbox
        self.hitbox_radius = self.size // 2
        
        # Estado
        self.active = False
        self.alive = True

        # Controle de drop
        self.has_dropped = False
        
        # Mutação (para implementar depois)
        self.is_mutated = False
    
    def spawn(self, x, y):
        """Ativa o inimigo"""
        self.x = x
        self.y = y
        self.active = True
        self.alive = True
        self.hp = self.max_hp
        self.rect.center = (self.x, self.y)
        self.has_dropped = False  # ✅ Resetar flag
    
    def update(self, dt, player_pos=None):
        """
        Atualiza o inimigo
        
        Args:
            dt (float): Delta time
            player_pos (tuple): Posição do player (x, y) - opcional
        """
        if not self.active or not self.alive:
            return
        
        # Movimento básico (subclasses podem sobrescrever)
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Atualizar rect
        self.rect.center = (self.x, self.y)
        
        # Desativar se sair da tela
        if self.y > SCREEN_HEIGHT + 50:
            self.deactivate()
        if self.x < -50 or self.x > SCREEN_WIDTH + 50:
            self.deactivate()
    
    def take_damage(self, amount):
        """Recebe dano"""
        if not self.alive:
            return False
        
        self.hp -= amount
        
        if self.hp <= 0:
            self.hp = 0
            self.die()
            return True  # ✅ Retorna True quando morre
        
        return False
    
    def die(self):
        """Inimigo morre"""
        self.alive = False
        self.hp = 0
        print(f"☠️ Enemy {self.enemy_type} morreu em ({self.x:.0f}, {self.y:.0f})")
    
    def deactivate(self):
        """Desativa o inimigo (retorna ao pool)"""
        self.active = False
        self.alive = False
    
    def render(self, screen):
        """
        Renderiza o inimigo
        
        Args:
            screen: Pygame surface
        """
        if not self.active:
            return
        
        # Renderizar sprite
        screen.blit(self.sprite, self.rect)
        
        # Debug: Hitbox
        from config import config
        if config.debug_mode and config.show_hitboxes:
            pygame.draw.circle(
                screen,
                COLOR_RED,
                (int(self.x), int(self.y)),
                self.hitbox_radius,
                1
            )
        
        # Debug: HP bar
        if config.debug_mode:
            self.render_hp_bar(screen)
    
    def render_hp_bar(self, screen):
        """Renderiza barra de HP (debug)"""
        bar_width = 30
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size // 2 - 8
        
        # Fundo (vermelho)
        pygame.draw.rect(
            screen,
            COLOR_RED,
            (bar_x, bar_y, bar_width, bar_height)
        )
        
        # HP atual (verde)
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(
            screen,
            COLOR_GREEN,
            (bar_x, bar_y, bar_width * hp_ratio, bar_height)
        )
    
    def get_collision_circle(self):
        """
        Retorna círculo de colisão
        
        Returns:
            tuple: (x, y, radius)
        """
        return (self.x, self.y, self.hitbox_radius)