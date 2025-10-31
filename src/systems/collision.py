"""
Collision System - Sistema de detecção de colisão
"""

import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class CollisionSystem:
    """Sistema de detecção de colisões"""
    
    @staticmethod
    def circle_collision(x1, y1, r1, x2, y2, r2):
        """
        Detecta colisão entre dois círculos
        
        Args:
            x1, y1, r1: Centro e raio do círculo 1
            x2, y2, r2: Centro e raio do círculo 2
            
        Returns:
            bool: True se colidindo
        """
        # Distância entre centros
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Colide se distância < soma dos raios
        return distance < (r1 + r2)
    
    @staticmethod
    def rect_collision(rect1, rect2):
        """
        Detecta colisão entre dois retângulos (pygame Rect)
        
        Args:
            rect1: pygame.Rect
            rect2: pygame.Rect
            
        Returns:
            bool: True se colidindo
        """
        return rect1.colliderect(rect2)
    
    @staticmethod
    def check_player_enemy_collision(player, enemy):
        """
        Verifica colisão entre player e inimigo (círculo)
        
        Args:
            player: Objeto Player
            enemy: Objeto Enemy
            
        Returns:
            bool: True se colidindo
        """
        if not enemy.active or not enemy.alive or not player.alive:
            return False
        
        return CollisionSystem.circle_collision(
            player.x, player.y, player.hitbox_radius,
            enemy.x, enemy.y, enemy.hitbox_radius
        )
    
    @staticmethod
    def check_projectile_enemy_collision(projectile, enemy):
        """
        Verifica colisão entre projétil e inimigo
        
        Args:
            projectile: Objeto Projectile
            enemy: Objeto Enemy
            
        Returns:
            bool: True se colidindo
        """
        if not projectile.active or not enemy.active or not enemy.alive:
            return False
        
        # Projéteis do player só colidem com inimigos
        if projectile.owner != 'player':
            return False
        
        # Usar retângulo para projétil (mais simples e justo)
        # Criar círculo virtual ao redor do projétil
        proj_radius = max(projectile.width, projectile.height) // 2
        
        return CollisionSystem.circle_collision(
            projectile.x, projectile.y, proj_radius,
            enemy.x, enemy.y, enemy.hitbox_radius
        )
    
    @staticmethod
    def check_projectile_player_collision(projectile, player):
        """
        Verifica colisão entre projétil inimigo e player
        
        Args:
            projectile: Objeto Projectile
            player: Objeto Player
            
        Returns:
            bool: True se colidindo
        """
        if not projectile.active or not player.alive:
            return False
        
        # Projéteis de inimigos só colidem com player
        if projectile.owner != 'enemy':
            return False
        
        proj_radius = max(projectile.width, projectile.height) // 2
        
        return CollisionSystem.circle_collision(
            projectile.x, projectile.y, proj_radius,
            player.x, player.y, player.hitbox_radius
        )
    
    @staticmethod
    def process_collisions(player, enemies, projectiles):
        """
        Processa todas as colisões do jogo
        
        Args:
            player: Objeto Player
            enemies: Lista de inimigos
            projectiles: ObjectPool de projéteis
            
        Returns:
            dict: Estatísticas de colisões
        """
        stats = {
            'player_hit': False,
            'enemies_hit': 0,
            'projectiles_destroyed': 0
        }
        
        # 1. Player vs Inimigos (colisão de corpo)
        for enemy in enemies:
            if CollisionSystem.check_player_enemy_collision(player, enemy):
                # Player toma dano
                if player.take_damage(enemy.damage):
                    stats['player_hit'] = True
                
                # Inimigo morre (kamikaze)
                enemy.take_damage(9999)
                stats['enemies_hit'] += 1
        
        # 2. Projéteis do Player vs Inimigos
        # ✅ NOVO: Implementar PIERCE corretamente
        for projectile in projectiles.in_use[:]:
            if not projectile.active or projectile.owner != 'player':
                continue
            
            # Contador de hits deste projétil neste frame
            hits_this_frame = 0
            max_hits = 1 + player.pierce  # 1 hit base + pierce adicional
            
            for enemy in enemies:
                if hits_this_frame >= max_hits:
                    break  # Já atingiu o máximo
                
                if CollisionSystem.check_projectile_enemy_collision(projectile, enemy):
                    # Inimigo toma dano
                    enemy.take_damage(projectile.damage)
                    stats['enemies_hit'] += 1
                    hits_this_frame += 1
                    
                    # Se atingiu máximo, destruir projétil
                    if hits_this_frame >= max_hits:
                        projectile.deactivate()
                        stats['projectiles_destroyed'] += 1
                        break
        
        # 3. Projéteis de Inimigos vs Player
        for projectile in projectiles.in_use[:]:
            if not projectile.active:
                continue
            
            if CollisionSystem.check_projectile_player_collision(projectile, player):
                # Player toma dano
                player.take_damage(projectile.damage)
                stats['player_hit'] = True
                
                # Projétil é destruído
                projectile.deactivate()
        
        return stats