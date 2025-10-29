"""
Collectible - Minérios que caem dos inimigos
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.utils.placeholder_generator import create_collectible_sprite


class Collectible:
    """Minério coletável"""
    
    def __init__(self):
        """Inicializa o minério"""
        self.x = 0
        self.y = 0
        self.value = 10
        
        # Movimento
        self.vy = 50  # Cai lentamente
        self.vx = 0
        
        # Visual
        self.size = 12
        self.sprite = create_collectible_sprite(self.size)
        self.rect = self.sprite.get_rect()
        
        # Hitbox
        self.radius = self.size // 2
        
        # Estado
        self.active = False
        self.lifetime = 15.0  # 15 segundos
        self.time_alive = 0
        
        # Piscar quando próximo de expirar
        self.blink_time = 10.0  # Começa a piscar aos 10s
        self.blink_state = False
        self.blink_timer = 0
    
    def spawn(self, x, y, value=10):
        """
        Ativa o minério
        
        Args:
            x (float): Posição X
            y (float): Posição Y
            value (int): Valor em minérios
        """
        self.x = x
        self.y = y
        self.value = value
        self.active = True
        self.time_alive = 0
        self.blink_state = False
        self.blink_timer = 0
        self.rect.center = (self.x, self.y)
        
        # Pequeno impulso aleatório
        import random
        self.vx = random.randint(-30, 30)
    
    def update(self, dt):
        """Atualiza o minério"""
        if not self.active:
            return
        
        # Movimento
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Atualizar rect
        self.rect.center = (self.x, self.y)
        
        # Lifetime
        self.time_alive += dt
        
        # Piscar quando próximo de expirar
        if self.time_alive >= self.blink_time:
            self.blink_timer += dt
            if self.blink_timer >= 0.2:  # Pisca a cada 0.2s
                self.blink_timer = 0
                self.blink_state = not self.blink_state
        
        # Expirar
        if self.time_alive >= self.lifetime:
            self.deactivate()
        
        # Sair da tela
        if self.y > SCREEN_HEIGHT + 50:
            self.deactivate()
    
    def deactivate(self):
        """Desativa o minério"""
        self.active = False
    
    def collect(self):
        """Coleta o minério"""
        self.deactivate()
        return self.value
    
    def render(self, screen):
        """Renderiza o minério"""
        if not self.active:
            return
        
        # Piscar quando próximo de expirar
        if self.time_alive >= self.blink_time and self.blink_state:
            return  # Não renderiza (efeito de piscar)
        
        screen.blit(self.sprite, self.rect)