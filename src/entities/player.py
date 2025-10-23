"""
Player - Nave controlada pelo jogador
"""

import pygame
import sys
import os

# Adiciona raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.utils.placeholder_generator import create_player_sprite


class Player:
    """Classe da nave do jogador"""
    
    def __init__(self, x, y):
        """
        Inicializa o player
        
        Args:
            x (int): Posição X inicial
            y (int): Posição Y inicial
        """
        # Posição
        self.x = x
        self.y = y
        
        # Velocidade (pixels por segundo)
        self.speed = 220  # Stats da nave inicial
        
        # Velocidade atual (para movimento suave)
        self.vx = 0
        self.vy = 0
        
        # Aceleração
        self.acceleration = 1200  # Pixels por segundo²
        self.deceleration = 800   # Pixels por segundo²
        
        # Stats base (nave inicial)
        self.max_hp = 100
        self.hp = 100
        self.damage = 10
        self.fire_rate = 0.25  # Segundos entre tiros
        self.fire_timer = 0
        
        # Sprite
        self.sprite = create_player_sprite(32)
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Hitbox (menor que sprite para gameplay justo)
        self.hitbox_radius = 12
        
        # Estado
        self.alive = True
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.5  # Segundos
        
    def handle_input(self, move_x, move_y):
        """
        Processa input de movimento
        
        Args:
            move_x (float): Movimento horizontal (-1 a 1)
            move_y (float): Movimento vertical (-1 a 1)
            
        Returns:
            tuple: (move_x, move_y) processados
        """
        return move_x, move_y
    
    def update(self, dt, move_x, move_y):
        """
        Atualiza o player
        
        Args:
            dt (float): Delta time em segundos
            move_x (float): Movimento horizontal (-1 a 1)
            move_y (float): Movimento vertical (-1 a 1)
        """
        if not self.alive:
            return
        
        # Input (já vem processado)
        moving_x, moving_y = self.handle_input(move_x, move_y)
        
        # Movimento com aceleração
        if moving_x != 0:
            # Acelerando
            self.vx += moving_x * self.acceleration * dt
            # Limitar velocidade máxima
            if abs(self.vx) > self.speed:
                self.vx = moving_x * self.speed
        else:
            # Desacelerando
            if self.vx > 0:
                self.vx -= self.deceleration * dt
                if self.vx < 0:
                    self.vx = 0
            elif self.vx < 0:
                self.vx += self.deceleration * dt
                if self.vx > 0:
                    self.vx = 0
        
        if moving_y != 0:
            # Acelerando
            self.vy += moving_y * self.acceleration * dt
            # Limitar velocidade máxima
            if abs(self.vy) > self.speed:
                self.vy = moving_y * self.speed
        else:
            # Desacelerando
            if self.vy > 0:
                self.vy -= self.deceleration * dt
                if self.vy < 0:
                    self.vy = 0
            elif self.vy < 0:
                self.vy += self.deceleration * dt
                if self.vy > 0:
                    self.vy = 0
        
        # Normalizar velocidade diagonal
        if moving_x != 0 and moving_y != 0:
            # Vetor diagonal normalizado (evita movimento mais rápido na diagonal)
            import math
            magnitude = math.sqrt(self.vx**2 + self.vy**2)
            if magnitude > self.speed:
                self.vx = (self.vx / magnitude) * self.speed
                self.vy = (self.vy / magnitude) * self.speed
        
        # Aplicar movimento
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Limites da tela
        self.x = max(PLAY_AREA_LEFT + 16, min(self.x, PLAY_AREA_RIGHT - 16))
        self.y = max(PLAY_AREA_TOP + 16, min(self.y, PLAY_AREA_BOTTOM - 16))
        
        # Atualizar rect
        self.rect.center = (self.x, self.y)
        
        # Invencibilidade
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Fire rate timer
        if self.fire_timer > 0:
            self.fire_timer -= dt
    
    def can_shoot(self):
        """Verifica se pode atirar"""
        return self.fire_timer <= 0
    
    def shoot(self):
        """Registra que atirou (reseta timer)"""
        self.fire_timer = self.fire_rate

    def create_projectile(self, projectile_pool):
        """
        Cria projétil (se puder atirar)
        
        Args:
            projectile_pool: Pool de projéteis
            
        Returns:
            bool: True se atirou, False se não pode
        """
        if not self.can_shoot():
            return False
        
        # Pegar projétil do pool
        projectile = projectile_pool.get()
        
        # Spawnar na posição do player (um pouco acima)
        projectile.spawn(
            x=self.x,
            y=self.y - 20,  # Acima do player
            damage=self.damage,
            owner='player'
        )
        
        # Resetar timer
        self.shoot()
        
        return True
    
    def take_damage(self, amount):
        """
        Recebe dano
        
        Args:
            amount (int): Quantidade de dano
        """
        if self.invincible or not self.alive:
            return False
        
        self.hp -= amount
        
        if self.hp <= 0:
            self.hp = 0
            self.die()
        else:
            # Ativar invencibilidade
            self.invincible = True
            self.invincible_timer = self.invincible_duration
        
        return True
    
    def die(self):
        """Player morre"""
        self.alive = False
        print("Player morreu!")
    
    def render(self, screen):
        """
        Renderiza o player
        
        Args:
            screen: Pygame surface
        """
        if not self.alive:
            return
        
        # Efeito de piscar quando invencível
        if self.invincible:
            # Pisca a cada 0.1s
            if int(self.invincible_timer * 10) % 2 == 0:
                return  # Não renderiza (pisca)
        
        # Renderizar sprite
        screen.blit(self.sprite, self.rect)
        
        # Debug: Hitbox (se debug ativo)
        from config import config
        if config.debug_mode and config.show_hitboxes:
            pygame.draw.circle(
                screen,
                COLOR_GREEN,
                (int(self.x), int(self.y)),
                self.hitbox_radius,
                1
            )