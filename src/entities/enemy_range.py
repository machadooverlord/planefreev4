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
        self.value = 20
        self.shoot_range = 400
        
        # Visual (azul para diferenciar)
        self.size = 32  # Maior que Kamikaze
        self.sprite = create_enemy_sprite(self.size, COLOR_BLUE)
        self.hitbox_radius = self.size // 2
        
        # Comportamento de tiro
        self.fire_rate = 2.0  # 1 tiro a cada 2 segundos
        self.fire_timer = 0
        self.can_shoot = False
        
        # ✅ NOVO: Movimento vertical em 3 fases
        self.stop_y = SCREEN_HEIGHT * 0.3  # Para em 30% da tela
        self.phase = 'descending'  # 'descending' → 'stopped' → 'leaving'
        self.stopped_timer = 0
        self.stopped_duration = 8.0  # ✅ Fica parado por 8 segundos
        
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
        self.phase = 'descending'
        self.stopped_timer = 0
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
        
        # Sistema de fases
        if self.phase == 'descending':
            # FASE 1: Descendo até stop_y
            self.vy = self.speed
            self.vx = 0
            
            # ✅ AI Level 2+: Pode atirar mesmo descendo (mas raramente)
            if self.ai_level >= 2:
                self.can_shoot = True
                # Aumenta fire rate (atira menos frequente)
                if self.fire_timer <= 0:
                    self.fire_rate = 4.0  # 1 tiro a cada 4s (metade da frequência)
            else:
                self.can_shoot = False
            
            if self.y >= self.stop_y:
                # Chegou no ponto de parada
                self.phase = 'stopped'
                self.stopped_timer = 0
                self.can_shoot = True
                self.fire_rate = 2.0  # Volta ao normal
                print(f"Range {id(self)} PAROU em Y={self.y:.0f}")
        
        elif self.phase == 'stopped':
            # FASE 2: Parado atirando MAS com movimento lateral
            self.vy = 0
            
            # Movimento lateral SEMPRE (não apenas AI 1+)
            import math
            self.vx = math.sin(pygame.time.get_ticks() * 0.002) * 40  # Patrol constante
            
            self.can_shoot = True
            self.fire_rate = 2.0
            
            # Contar tempo parado
            self.stopped_timer += dt
            
            if self.stopped_timer >= self.stopped_duration:
                # Acabou o tempo, começar a descer
                self.phase = 'leaving'
                print(f"Range {id(self)} voltou a DESCER")
        
        elif self.phase == 'leaving':
            # FASE 3: Descendo até sair da tela
            self.vy = self.speed
            self.vx = 0
            
            # ✅ AI Level 2+: Continua atirando em retirada (menos frequente)
            if self.ai_level >= 2:
                self.can_shoot = True
                self.fire_rate = 5.0  # 1 tiro a cada 5s (bem raro)
            else:
                self.can_shoot = False
    
        # Aplicar movimento
        super().update(dt, player_pos)
        
        # Fire rate timer
        if self.fire_timer > 0:
            self.fire_timer -= dt
        else:
            self.fire_timer = 0
    
    def can_fire(self):
        """
        Verifica se pode atirar
        
        Returns:
            bool: True se pode atirar
        """
        return (
            self.can_shoot and 
            self.fire_timer <= 0 and 
            self.alive and 
            self.active and
            self.phase == 'stopped'  # ✅ Só atira quando parado
        )
    
    def shoot(self, projectile_pool, player_pos=None):
        if not self.can_fire():
            return False
        
        # Verificar se player está no alcance
        if player_pos:
            import math
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Alcance aumenta com AI level
            effective_range = self.shoot_range + (self.ai_level * 100)
            
            if distance > effective_range:
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