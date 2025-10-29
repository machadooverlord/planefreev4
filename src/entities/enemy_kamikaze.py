"""
Enemy Kamikaze - Inimigo que desce rapidamente (suicida)
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.entities.enemy import Enemy
from src.utils.placeholder_generator import create_enemy_sprite


class EnemyKamikaze(Enemy):
    """Inimigo Kamikaze - rápido e direto"""
    
    def __init__(self):
        """Inicializa o Kamikaze"""
        super().__init__(0, 0, enemy_type='kamikaze')
        
        # Stats específicos do Kamikaze (Setor 1 base)
        self.max_hp = 30
        self.hp = 30
        self.speed = 150  # Mais rápido que a base
        self.damage = 20
        self.value = 10
        
        # Visual
        self.size = 24
        self.sprite = create_enemy_sprite(self.size, COLOR_RED)
        self.hitbox_radius = self.size // 2
        
        # Comportamento
        self.ai_level = 0  # 0 = movimento linear
    
    def update(self, dt, player_pos=None):
        """
        Atualiza o Kamikaze
        
        Args:
            dt (float): Delta time
            player_pos (tuple): Posição do player (x, y)
        """
        if not self.active or not self.alive:
            return
        
        # Comportamento baseado no AI level
        if self.ai_level == 0:
            # Nível 0: Desce mas com LEVE correção para o player
            self.vy = self.speed
            
            if player_pos:
                player_x, player_y = player_pos
                
                # Correção MUITO LEVE (10% da velocidade)
                if abs(self.x - player_x) > 20:
                    if self.x < player_x:
                        self.vx = self.speed * 0.1
                    else:
                        self.vx = -self.speed * 0.1
                else:
                    self.vx = 0
            else:
                self.vx = 0
        
        elif self.ai_level == 1 and player_pos:
            # Nível 1: Leve correção lateral em direção ao player
            player_x, player_y = player_pos
            
            # Movimento principal: para baixo
            self.vy = self.speed
            
            # Correção lateral suave (30% da velocidade)
            if abs(self.x - player_x) > 10:  # Deadzone
                if self.x < player_x:
                    self.vx = self.speed * 0.3
                else:
                    self.vx = -self.speed * 0.3
            else:
                self.vx = 0
        
        elif self.ai_level >= 2 and player_pos:
            # Nível 2+: Zigzag em direção ao player
            player_x, player_y = player_pos
            
            # Movimento base
            self.vy = self.speed
            
            # Zigzag
            import math
            zigzag_frequency = 3.0  # Frequência do zigzag
            zigzag_amplitude = 50   # Amplitude do zigzag
            
            # Usa Y como "tempo" para o zigzag
            zigzag_offset = math.sin(self.y * zigzag_frequency * 0.01) * zigzag_amplitude
            
            # Direção geral para o player + zigzag
            if abs(self.x - player_x) > 10:
                direction = 1 if self.x < player_x else -1
                self.vx = (direction * self.speed * 0.4) + (zigzag_offset * dt)
            else:
                self.vx = zigzag_offset * dt
        
        # Aplicar movimento (chamar método da classe pai)
        super().update(dt, player_pos)
    
    def set_ai_level(self, level):
        """
        Define nível de IA
        
        Args:
            level (int): 0 = linear, 1 = tracking leve, 2+ = zigzag
        """
        self.ai_level = level