"""
Enemy Mother - Inimigo que spawna mini-inimigos
"""

import pygame
import random
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *
from src.entities.enemy import Enemy
from src.utils.placeholder_generator import create_enemy_sprite


class EnemyMother(Enemy):
    """Inimigo Mãe - spawna mini-inimigos orbitais"""
    
    def __init__(self):
        """Inicializa a Mãe"""
        super().__init__(0, 0, enemy_type='mother')
        
        # Stats específicos da Mãe (Setor 1 base)
        self.max_hp = 100
        self.hp = 100
        self.speed = 40  # Lenta
        self.damage = 25
        self.value = 50  # 5 minérios de 10
        
        # Visual (roxo grande)
        self.size = 48
        self.sprite = create_enemy_sprite(self.size, (150, 0, 200))
        self.hitbox_radius = self.size // 2
        
        # Spawning de filhotes
        self.spawn_rate = 5.0  # 1 filhote a cada 5s
        self.spawn_timer = 0
        self.max_children = 4
        self.children = []  # Lista de filhotes (objetos Enemy)
        
        # Órbitas dos filhotes
        self.child_angles = []  # Ângulos de cada filhote
        self.orbit_radius = 60
        self.orbit_speed = 60  # Graus por segundo
        
        # IA
        self.ai_level = 0
        
        print(f"✅ Mother criada")
    
    def spawn(self, x, y):
        """Spawna a Mãe"""
        super().spawn(x, y)
        self.spawn_timer = self.spawn_rate
        self.children = []
        self.child_angles = []
        print(f"👪 Mother spawnada em ({x:.0f}, {y:.0f})")
    
    def update(self, dt, player_pos=None):
        """Atualiza a Mãe"""
        if not self.active or not self.alive:
            return
        
        # Sempre desce (como Kamikaze mas mais lento)
        self.vy = self.speed
        
        # Patrol lateral
        self.vx = math.sin(pygame.time.get_ticks() * 0.001) * 25
        
        # Aplicar movimento
        super().update(dt, player_pos)
        
        # ✅ Atualizar posições orbitais dos filhotes
        for i, child in enumerate(self.children[:]):
            if not child.alive or not child.active:
                # Remover mortos
                self.children.remove(child)
                if i < len(self.child_angles):
                    self.child_angles.pop(i)
                continue
            
            # Atualizar ângulo orbital
            if i < len(self.child_angles):
                self.child_angles[i] += self.orbit_speed * dt
                if self.child_angles[i] >= 360:
                    self.child_angles[i] -= 360
                
                # Calcular posição orbital
                angle_rad = math.radians(self.child_angles[i])
                child.x = self.x + math.cos(angle_rad) * self.orbit_radius
                child.y = self.y + math.sin(angle_rad) * self.orbit_radius
                
                # Atualizar rect
                child.rect.center = (child.x, child.y)
        
        # Spawn timer
        if self.spawn_timer > 0:
            self.spawn_timer -= dt
    
    def can_spawn_child(self):
        """Verifica se pode spawnar filhote"""
        can_spawn = (
            self.spawn_timer <= 0 and
            len(self.children) < self.max_children and
            self.alive and
            self.active
        )
        
        if can_spawn and self.spawn_timer <= 0:
            print(f"👶 Mother pode spawnar! (Filhotes: {len(self.children)}/{self.max_children})")
        
        return can_spawn
    
    def spawn_child(self, child):
        """
        Spawna um filhote orbital
        
        Args:
            child: Objeto Enemy (Kamikaze ou Range do pool)
        
        Returns:
            bool: True se spawnou
        """
        if not self.can_spawn_child():
            return False
        
        # Spawnar na posição da mãe
        child.spawn(self.x, self.y)
        
        # ✅ Reduzir stats (1/3)
        child.max_hp = max(10, child.max_hp // 3)
        child.hp = child.max_hp
        child.speed = max(50, child.speed // 3)
        child.damage = max(5, child.damage // 3)
        child.value = max(3, child.value // 3)
        
        # Visual menor
        child.size = 16
        # Cor baseada no tipo
        if child.enemy_type == 'kamikaze':
            child.sprite = create_enemy_sprite(16, (255, 100, 100))  # Vermelho claro
        else:
            child.sprite = create_enemy_sprite(16, (100, 100, 255))  # Azul claro
        
        child.hitbox_radius = child.size // 2
        child.rect = child.sprite.get_rect()
        child.rect.center = (child.x, child.y)
        
        # Adicionar à lista
        self.children.append(child)
        
        # Ângulo orbital inicial aleatório
        self.child_angles.append(random.uniform(0, 360))
        
        # Reset timer
        self.spawn_timer = self.spawn_rate
        
        print(f"✅ Mother spawnou filhote {child.enemy_type} (Total: {len(self.children)})")
        
        return True
    
    def die(self):
        """Mãe morre - filhotes morrem junto"""
        self.alive = False
        
        # Matar todos filhotes
        for child in self.children:
            if child.alive:
                child.take_damage(9999)
                print(f"  ☠️ Filhote {child.enemy_type} morreu junto")
        
        self.children = []
        self.child_angles = []
        
        print(f"☠️ Mother morreu! Filhotes eliminados")
    
    def set_ai_level(self, level):
        """Define nível de IA"""
        self.ai_level = level
        
        # Ajustar comportamento
        if level >= 2:
            self.spawn_rate = 4.0  # Spawna mais rápido
            self.max_children = 5
        if level >= 4:
            self.spawn_rate = 3.0
            self.max_children = 6