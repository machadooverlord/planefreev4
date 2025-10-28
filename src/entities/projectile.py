"""
Projectile - Projéteis disparados pelo player e inimigos
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.utils.placeholder_generator import create_projectile_sprite


class Projectile:
    """Classe de projétil"""
    
    def __init__(self):
        """Inicializa projétil"""
        # Posição
        self.x = 0
        self.y = 0
        
        # Velocidade
        self.vx = 0
        self.vy = -600  # Para cima (pixels/s)
        
        # Stats
        self.damage = 10
        
        # Sprites (criados uma vez)
        self.sprite_player = create_projectile_sprite(6, 12, COLOR_YELLOW)
        self.sprite_enemy = create_projectile_sprite(8, 8, COLOR_RED)
        self.sprite = self.sprite_player  # Padrão
        self.rect = self.sprite.get_rect()
        
        # Hitbox
        self.width = 6
        self.height = 12
        
        # Estado
        self.active = False
        self.lifetime = 2.0  # Segundos
        self.time_alive = 0
        
        # Tipo (para diferenciar player vs inimigo)
        self.owner = 'player'  # 'player' ou 'enemy'
    
    def spawn(self, x, y, damage=10, owner='player'):
        """
        Ativa o projétil
        
        Args:
            x (float): Posição X inicial
            y (float): Posição Y inicial
            damage (int): Dano que causa
            owner (str): 'player' ou 'enemy'
        """
        self.x = x
        self.y = y
        self.damage = damage
        self.owner = owner
        self.active = True
        self.time_alive = 0
        
        # ✅ CONFIGURAR VELOCIDADE BASEADO NO OWNER
        if owner == 'player':
            # Projéteis do player: PARA CIMA
            self.vx = 0
            self.vy = -600  # ✅ NEGATIVO = para cima
            
            # Configurar sprite
            self.sprite = self.sprite_player
            self.width = 6
            self.height = 12
            self.rect = self.sprite.get_rect()
        
        else:  # enemy
            # Projéteis inimigos: Velocidade será setada por quem chamou
            # (já vem configurado pelo enemy_range.shoot())
            
            # Configurar sprite
            self.sprite = self.sprite_enemy
            self.width = 8
            self.height = 8
            self.rect = self.sprite.get_rect()
        
        self.rect.center = (self.x, self.y)
    
    def update(self, dt):
        """
        Atualiza projétil
        
        Args:
            dt (float): Delta time em segundos
        """
        if not self.active:
            return
        
        # Movimento
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Atualizar rect
        self.rect.center = (self.x, self.y)
        
        # Lifetime
        self.time_alive += dt
        if self.time_alive >= self.lifetime:
            self.deactivate()
        
        # Sair da tela
        if self.y < -20 or self.y > SCREEN_HEIGHT + 20:
            self.deactivate()
        if self.x < -20 or self.x > SCREEN_WIDTH + 20:
            self.deactivate()
    
    def deactivate(self):
        """Desativa o projétil (retorna ao pool)"""
        self.active = False
        # ✅ NÃO resetar sprite aqui - será feito no próximo spawn()
    
    def render(self, screen):
        """
        Renderiza o projétil
        
        Args:
            screen: Pygame surface
        """
        if not self.active:
            return
        
        screen.blit(self.sprite, self.rect)
        
        # Debug: Hitbox
        from config import config
        if config.debug_mode and config.show_hitboxes:
            pygame.draw.rect(
                screen,
                COLOR_YELLOW if self.owner == 'player' else COLOR_RED,
                self.rect,
                1
            )