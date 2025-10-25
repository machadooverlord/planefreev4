"""
Enemy Range - Inimigo que ataca de longe
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.entities.enemy import Enemy
from src.utils.placeholder_generator import create_enemy_sprite


class EnemyRange(Enemy):
    """Inimigo Range - ataca de longe, move-se lentamente"""
    
    def __init__(self):
        """Inicializa o Range"""
        super().__init__(0, 0, enemy_type='range')
        
        # Stats específicos do Range (Setor 1 base)
        self.max_hp = 45
        self.hp = 45
        self.speed = 60  # Mais lento que Kamikaze
        self.damage = 10  # Dano do projétil
        self.value = 17  # 15-20 minérios (média)
        
        # Visual (azul para diferenciar)
        self.size = 32  # Maior que Kamikaze
        self.sprite = create_enemy_sprite(self.size, COLOR_BLUE)
        self.hitbox_radius = self.size // 2
        
        # Comportamento de tiro
        self.fire_rate = 2.0  # 1 tiro a cada 2 segundos
        self.fire_timer = 0
        self.can_shoot = False
        
        # Movimento vertical
        self.stop_y = SCREEN_HEIGHT * 0.3  # Para em 30% da tela
        self.has_stopped = False
        
        # IA
        self.ai_level = 0
    
    def spawn(self, x, y):
        """
        Spawna o Range
        
        Args:
            x (float): Posição X
            y (float): Posição Y
        """
        super().spawn(x, y)
        self.fire_timer = self.fire_rate  # Começa pronto para atirar
        self.has_stopped = False
        self.can_shoot = False
    
    def update(self, dt, player_pos=None):
        """
        Atualiza o Range
        
        Args:
            dt (float): Delta time
            player_pos (tuple): Posição do player (x, y)
        """
        if not self.active or not self.alive:
            return
        
        # Movimento vertical (desce até stop_y, depois para)
        if not self.has_stopped:
            if self.y < self.stop_y:
                self.vy = self.speed
            else:
                self.vy = 0
                self.has_stopped = True
                self.can_shoot = True
        else:
            # Movimento lateral leve (patrol)
            if self.ai_level >= 1:
                import math
                # Movimento senoidal suave
                self.vx = math.sin(pygame.time.get_ticks() * 0.001) * 30
            else:
                self.vx = 0
        
        # Aplicar movimento
        super().update(dt, player_pos)
        
        # Fire rate timer
        if self.fire_timer > 0:
            self.fire_timer -= dt
    
    def can_fire(self):
        """
        Verifica se pode atirar
        
        Returns:
            bool: True se pode atirar
        """
        return self.can_shoot and self.fire_timer <= 0 and self.alive and self.active
    
    def shoot(self, projectile_pool, player_pos=None):
        """
        Atira um projétil
        
        Args:
            projectile_pool: Pool de projéteis
            player_pos (tuple): Posição do player para mirar
            
        Returns:
            bool: True se atirou
        """
        if not self.can_fire():
            return False
        
        # Pegar projétil do pool
        projectile = projectile_pool.get()
        
        # AI Level determina padrão de tiro
        if self.ai_level == 0:
            # Level 0: Atira reto para baixo
            projectile.spawn(
                x=self.x,
                y=self.y + self.size // 2,
                damage=self.damage,
                owner='enemy'
            )
            projectile.vx = 0
            projectile.vy = 200  # Para baixo
        
        elif self.ai_level >= 1 and player_pos:
            # Level 1+: Mira no player
            import math
            
            # Calcular direção para o player
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Normalizar e aplicar velocidade
                speed = 250
                projectile.spawn(
                    x=self.x,
                    y=self.y + self.size // 2,
                    damage=self.damage,
                    owner='enemy'
                )
                projectile.vx = (dx / distance) * speed
                projectile.vy = (dy / distance) * speed
        
        # Reset timer
        self.fire_timer = self.fire_rate
        
        return True
    
    def set_ai_level(self, level):
        """
        Define nível de IA
        
        Args:
            level (int): 0 = tiro reto, 1+ = mira no player
        """
        self.ai_level = level
    
    def render(self, screen):
        """
        Renderiza o Range (com indicador de tiro)
        
        Args:
            screen: Pygame surface
        """
        super().render(screen)
        
        # Indicador visual quando pronto para atirar
        from config import config
        if config.debug_mode and self.can_shoot and self.fire_timer <= 0.5:
            # Flash vermelho quando quase atirar
            pygame.draw.circle(
                screen,
                COLOR_RED,
                (int(self.x), int(self.y)),
                self.hitbox_radius + 5,
                2
            )