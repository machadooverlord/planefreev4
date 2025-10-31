"""
CardDrop - Carta que cai de inimigos e pode ser coletada
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *


class CardDrop:
    """Carta coletável que cai de inimigos"""
    
    def __init__(self):
        """Inicializa o drop de carta"""
        self.x = 0
        self.y = 0
        self.card = None  # Objeto Card
        
        # Movimento
        self.vy = 50  # Cai lentamente
        self.vx = 0
        
        # Visual
        self.size = 32  # Tamanho do sprite da carta
        self.sprite = None  # Será criado quando spawnar
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        
        # Animação de flutuação
        self.float_offset = 0
        self.float_speed = 2.0  # Velocidade da flutuação
        self.float_amplitude = 4  # Altura da flutuação
        
        # Brilho/pulsação
        self.pulse_timer = 0
        self.pulse_speed = 3.0
        
        # Hitbox para coleta
        self.collect_radius = 40
        
        # Estado
        self.active = False
        self.lifetime = 30.0  # 30 segundos antes de desaparecer
        self.time_alive = 0
        
        # Piscar quando próximo de expirar
        self.blink_time = 20.0  # Começa a piscar aos 20s
        self.blink_state = False
        self.blink_timer = 0
        
        # Input de coleta
        self.can_collect = True
        self.collect_cooldown = 0.5  # Meio segundo entre coletas
        self.collect_timer = 0
    
    def spawn(self, x, y, card):
        """
        Ativa o drop de carta
        
        Args:
            x (float): Posição X
            y (float): Posição Y
            card (Card): Objeto Card a ser dropado
        """
        self.x = x
        self.y = y
        self.card = card
        self.active = True
        self.time_alive = 0
        self.blink_state = False
        self.blink_timer = 0
        self.float_offset = 0
        self.pulse_timer = 0
        self.can_collect = True
        self.collect_timer = 0
        
        # Criar sprite da carta
        self._create_sprite()
        
        # Pequeno impulso aleatório
        import random
        self.vx = random.randint(-30, 30)
        
        self.rect.center = (self.x, self.y)
        
        print(f"🃏 Carta dropada: {card.name} ({card.rarity}) em ({x:.0f}, {y:.0f})")
    
    def _create_sprite(self):
        """Cria sprite visual da carta"""
        # Surface com transparência
        self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Cor da borda baseada na raridade
        rarity_color = self.card.get_rarity_color()
        
        # Fundo escuro (quase preto)
        pygame.draw.rect(
            self.sprite,
            (20, 20, 20),
            (2, 2, self.size - 4, self.size - 4)
        )
        
        # Borda grossa colorida (raridade)
        pygame.draw.rect(
            self.sprite,
            rarity_color,
            (0, 0, self.size, self.size),
            3  # Espessura da borda
        )
        
        # Símbolo no centro (baseado no tipo)
        center = self.size // 2
        
        if self.card.type == 'passive':
            # Círculo para passivas
            pygame.draw.circle(
                self.sprite,
                rarity_color,
                (center, center),
                8
            )
        elif self.card.type == 'active':
            # Estrela para ativas
            pygame.draw.polygon(
                self.sprite,
                rarity_color,
                [
                    (center, center - 8),
                    (center + 3, center - 2),
                    (center + 8, center),
                    (center + 3, center + 3),
                    (center, center + 8),
                    (center - 3, center + 3),
                    (center - 8, center),
                    (center - 3, center - 2),
                ]
            )
    
    def update(self, dt):
        """Atualiza o drop de carta"""
        if not self.active:
            return
        
        # Movimento
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Desacelerar movimento horizontal
        if abs(self.vx) > 0:
            self.vx *= 0.95
        
        # Desacelerar movimento vertical (para de cair)
        if self.vy > 0:
            self.vy *= 0.90
            if self.vy < 5:
                self.vy = 0
        
        # Animação de flutuação (quando parado)
        if self.vy == 0:
            import math
            self.float_offset = math.sin(pygame.time.get_ticks() * 0.001 * self.float_speed) * self.float_amplitude
        
        # Pulsação do brilho
        self.pulse_timer += dt * self.pulse_speed
        
        # Atualizar rect (com flutuação)
        self.rect.center = (self.x, self.y + self.float_offset)
        
        # Lifetime
        self.time_alive += dt
        
        # Piscar quando próximo de expirar
        if self.time_alive >= self.blink_time:
            self.blink_timer += dt
            if self.blink_timer >= 0.3:  # Pisca a cada 0.3s
                self.blink_timer = 0
                self.blink_state = not self.blink_state
        
        # Expirar
        if self.time_alive >= self.lifetime:
            self.deactivate()
            print(f"⏱️ Carta {self.card.name if self.card else 'Unknown'} expirou")
        
        # Sair da tela (para baixo)
        if self.y > SCREEN_HEIGHT + 50:
            self.deactivate()
        
        # Cooldown de coleta
        if not self.can_collect:
            self.collect_timer += dt
            if self.collect_timer >= self.collect_cooldown:
                self.can_collect = True
                self.collect_timer = 0
    
    def deactivate(self):
        """Desativa o drop"""
        self.active = False
        self.card = None
    
    def collect(self, player):
        """
        Tenta coletar a carta
        
        Args:
            player: Objeto Player
            
        Returns:
            bool: True se coletou, False se slots cheios
        """
        if not self.active or not self.can_collect or self.card is None:
            return False
        
        # Verificar se player pode equipar
        if len(player.equipped_cards) >= player.max_card_slots:
            print(f"❌ Slots cheios! ({len(player.equipped_cards)}/{player.max_card_slots})")
            # TODO: Abrir menu de troca de cartas
            return False
        
        # Guardar referência da carta ANTES de desativar
        card_name = self.card.name
        
        # Equipar carta
        success = player.equip_card(self.card)
        
        if success:
            print(f"✅ Carta coletada: {card_name}")
            self.deactivate()
            return True
        
        return False
    
    def check_collect_input(self, input_manager, player):
        """
        Verifica se player está tentando coletar
        
        Args:
            input_manager: InputManager
            player: Player
            
        Returns:
            bool: True se coletou
        """
        if not self.active or not self.can_collect or self.card is None:
            return False
        
        # Verificar distância
        dx = self.x - player.x
        dy = self.y - player.y
        distance_sq = dx*dx + dy*dy
        
        if distance_sq > self.collect_radius * self.collect_radius:
            return False
        
        # Verificar input (E ou botão A)
        collect_pressed = (
            input_manager.is_key_pressed(pygame.K_e) or
            input_manager.get_button('A', 0)
        )
        
        if collect_pressed:
            collected = self.collect(player)
            if collected:
                # Impedir múltiplas coletas
                self.can_collect = False
            return collected
        
        return False
    
    def render(self, screen):
        """Renderiza o drop de carta"""
        if not self.active:
            return
        
        # Piscar quando próximo de expirar
        if self.time_alive >= self.blink_time and self.blink_state:
            return  # Não renderiza (efeito de piscar)
        
        # Renderizar sprite
        screen.blit(self.sprite, self.rect)
        
        # Brilho/pulsação (círculo em volta)
        import math
        pulse_alpha = int((math.sin(self.pulse_timer) * 0.5 + 0.5) * 100) + 50  # 50-150
        pulse_radius = self.size // 2 + 4
        
        # Surface temporária para brilho
        glow_surface = pygame.Surface((self.size + 20, self.size + 20), pygame.SRCALPHA)
        rarity_color = self.card.get_rarity_color()
        glow_color = (*rarity_color, pulse_alpha)
        
        pygame.draw.circle(
            glow_surface,
            glow_color,
            (self.size // 2 + 10, self.size // 2 + 10),
            pulse_radius,
            2
        )
        
        screen.blit(
            glow_surface,
            (self.rect.x - 10, self.rect.y - 10)
        )
    
    def render_collect_prompt(self, screen, player):
        """
        Renderiza prompt de coleta quando player está perto
        
        Args:
            screen: Pygame surface
            player: Player
        """
        if not self.active or self.card is None:
            return
        
        # Verificar distância
        dx = self.x - player.x
        dy = self.y - player.y
        distance_sq = dx*dx + dy*dy
        
        if distance_sq > self.collect_radius * self.collect_radius:
            return
        
        # Prompt "Pressione E para coletar"
        font = pygame.font.Font(None, 20)
        text = font.render("[E] Coletar", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(self.x, self.y - self.size))
        
        # Fundo semi-transparente
        bg_rect = text_rect.inflate(10, 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        
        screen.blit(bg_surface, bg_rect)
        screen.blit(text, text_rect)
        
        # Nome da carta
        font_small = pygame.font.Font(None, 16)
        name_text = font_small.render(self.card.name, True, self.card.get_rarity_color())
        name_rect = name_text.get_rect(center=(self.x, self.y + self.size + 5))
        
        screen.blit(name_text, name_rect)