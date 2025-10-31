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

        # Regeneração de vida
        self.regen_rate = 0.5  # HP por segundo (será modificado por classe)
        self.regen_timer = 0
        self.regen_interval = 1.0  # Regenera a cada 1 segundo

        # Sistema de cartas
        self.equipped_cards = []  # Lista de Card objects
        self.max_card_slots = 3   # Máximo de cartas equipadas
        
        # Stats modificáveis por cartas
        self.pierce = 0  # Quantos inimigos projétil atravessa
        self.projectile_count = 1  # Quantos projéteis atira
        self.lifesteal = 0.0  # % de dano que vira HP
        self.shield = 0  # Bloqueia hits
        self.shield_timer = 0
        self.shield_cooldown = 10.0
        self.explosion_radius = 0  # Raio de explosão dos projéteis
        
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

        # Regeneração de vida
        if self.hp < self.max_hp:
            self.regen_timer += dt
            
            if self.regen_timer >= self.regen_interval:
                self.regen_timer = 0
                
                # Regenerar
                self.hp += self.regen_rate
                
                # Não ultrapassar máximo
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                
                # Debug (apenas quando regenera)
                if int(self.hp) % 5 == 0:  # A cada 5 HP
                    print(f"♥️ Regenerou! HP: {int(self.hp)}/{self.max_hp}")
        
        # Invencibilidade
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Fire rate timer
        if self.fire_timer > 0:
            self.fire_timer -= dt
        else:
            self.fire_timer = 0
    
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
        
        # Spawnar no NARIZ
        # Sprite do player = 32px altura
        # Triângulo aponta para CIMA (Y negativo)
        # Centro do sprite está em self.y
        # Nariz está 16 pixels ACIMA (y - 16)
        
        projectile.spawn(
            x=self.x,
            y=self.y - 16,  # Subtrair metade do sprite (32 / 2 = 16)
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

    def set_ship_class(self, ship_class):
        """
        Define classe da nave (afeta regeneração)
        
        Args:
            ship_class (str): 'tanque', 'velocista', 'tecnico'
        """
        if ship_class == 'tanque':
            self.regen_rate = 1.0  # 1 HP/s (mais rápido)
        elif ship_class == 'velocista':
            self.regen_rate = 0.3  # 0.3 HP/s (mais lento)
        elif ship_class == 'tecnico':
            self.regen_rate = 0.5  # 0.5 HP/s (balanceado)
        
        print(f"✨ Classe: {ship_class} | Regen: {self.regen_rate} HP/s")
    
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
            if int(self.invincible_timer * 10) % 2 == 0:
                return
        
        # Renderizar sprite
        screen.blit(self.sprite, self.rect)
        
        # DEBUG: Mostrar onde projétil spawna
        from config import config
        if config.debug_mode:
            # Ponto de spawn do projétil (nariz)
            spawn_y = self.y - 16
            pygame.draw.circle(
                screen,
                (255, 0, 255),  # Rosa/Magenta
                (int(self.x), int(spawn_y)),
                4,  # Raio
                0   # Preenchido
            )
            
            # Linha do centro do player
            pygame.draw.line(
                screen,
                (0, 255, 255),  # Ciano
                (int(self.x) - 10, int(self.y)),
                (int(self.x) + 10, int(self.y)),
                2
            )
        
        # Hitbox
        if config.debug_mode and config.show_hitboxes:
            pygame.draw.circle(
                screen,
                COLOR_GREEN,
                (int(self.x), int(self.y)),
                self.hitbox_radius,
                1
            )
    
    def equip_card(self, card):
        """
        Equipa uma carta
        
        Args:
            card (Card): Carta a equipar
            
        Returns:
            bool: True se equipou
        """
        if len(self.equipped_cards) >= self.max_card_slots:
            print(f"❌ Slots cheios! ({len(self.equipped_cards)}/{self.max_card_slots})")
            return False
        
        # Aplicar efeito
        card.apply_effect(self)
        
        # Adicionar à lista
        self.equipped_cards.append(card)
        
        print(f"✅ Carta equipada: {card.name} ({len(self.equipped_cards)}/{self.max_card_slots})")
        
        return True

    def unequip_card(self, card):
        """
        Desequipa uma carta
        
        Args:
            card (Card): Carta a desequipar
        """
        if card in self.equipped_cards:
            # Remover efeito
            card.remove_effect(self)
            
            # Remover da lista
            self.equipped_cards.remove(card)
            
            print(f"❌ Carta removida: {card.name}")