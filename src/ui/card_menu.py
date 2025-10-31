"""
CardMenu - Menu de gerenciamento de cartas equipadas
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *


class CardMenu:
    """Menu para visualizar e gerenciar cartas equipadas"""
    
    def __init__(self):
        """Inicializa o menu de cartas"""
        # Estado
        self.active = False
        self.selected_slot = 0  # Slot selecionado (0-2)
        
        # Layout
        self.menu_width = 600
        self.menu_height = 500
        self.menu_x = (SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = (SCREEN_HEIGHT - self.menu_height) // 2
        
        # Slots de cartas
        self.slot_height = 120
        self.slot_spacing = 20
        
        # Fontes
        self.font_title = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Cores
        self.bg_color = (20, 20, 30, 230)  # Fundo escuro semi-transparente
        self.border_color = (100, 100, 150)
        self.selected_color = (255, 255, 100)
        
        # Input cooldown (para evitar múltiplos inputs)
        self.input_cooldown = 0.2
        self.input_timer = 0
        self.can_input = True
        
        # Confirmação de remoção
        self.confirming_removal = False
        self.removal_timer = 0
        self.removal_duration = 2.0
    
    def toggle(self):
        """Abre/fecha o menu"""
        self.active = not self.active
        self.selected_slot = 0
        self.confirming_removal = False
        print(f"📋 Card Menu: {'ABERTO' if self.active else 'FECHADO'}")
    
    def open(self):
        """Abre o menu"""
        self.active = True
        self.selected_slot = 0
        self.confirming_removal = False
        print("📋 Card Menu ABERTO")
    
    def close(self):
        """Fecha o menu"""
        self.active = False
        self.confirming_removal = False
        print("📋 Card Menu FECHADO")
    
    def update(self, dt, input_manager, player):
        """
        Atualiza o menu
        
        Args:
            dt (float): Delta time
            input_manager: InputManager
            player: Player object
        """
        if not self.active:
            return
        
        # Input cooldown
        if not self.can_input:
            self.input_timer += dt
            if self.input_timer >= self.input_cooldown:
                self.can_input = True
                self.input_timer = 0
        
        # Timer de confirmação de remoção
        if self.confirming_removal:
            self.removal_timer += dt
            if self.removal_timer >= self.removal_duration:
                self.confirming_removal = False
                self.removal_timer = 0
        
        # Processar input apenas se pode
        if self.can_input:
            self._handle_input(input_manager, player)
    
    def _handle_input(self, input_manager, player):
        """Processa input do menu"""
        # Navegação: Setas ou D-pad
        move_x, move_y = input_manager.get_movement(player_index=0)
        
        if move_y < -0.5:  # Para cima
            self.selected_slot = max(0, self.selected_slot - 1)
            self.can_input = False
            self.confirming_removal = False
            print(f"⬆️ Slot selecionado: {self.selected_slot}")
        
        elif move_y > 0.5:  # Para baixo
            max_slot = min(2, len(player.equipped_cards) - 1)
            self.selected_slot = min(max_slot, self.selected_slot + 1)
            self.can_input = False
            self.confirming_removal = False
            print(f"⬇️ Slot selecionado: {self.selected_slot}")
        
        # Remover carta: Tecla R ou Botão B
        remove_pressed = (
            input_manager.is_key_pressed(pygame.K_r) or
            input_manager.get_button('B', 0)
        )
        
        if remove_pressed:
            if len(player.equipped_cards) > self.selected_slot:
                if not self.confirming_removal:
                    # Primeira vez: pedir confirmação
                    self.confirming_removal = True
                    self.removal_timer = 0
                    self.can_input = False
                    print(f"⚠️ Pressione R novamente para confirmar remoção")
                else:
                    # Segunda vez: remover carta
                    card = player.equipped_cards[self.selected_slot]
                    player.unequip_card(card)
                    self.confirming_removal = False
                    self.can_input = False
                    
                    # Ajustar seleção se necessário
                    if self.selected_slot >= len(player.equipped_cards):
                        self.selected_slot = max(0, len(player.equipped_cards) - 1)
                    
                    print(f"🗑️ Carta removida: {card.name}")
        
        # Fechar menu: TAB ou START
        close_pressed = (
            input_manager.is_key_pressed(pygame.K_TAB) or
            input_manager.get_button('START', 0)
        )
        
        if close_pressed:
            self.close()
            self.can_input = False
    
    def render(self, screen, player):
        """
        Renderiza o menu
        
        Args:
            screen: Pygame surface
            player: Player object
        """
        if not self.active:
            return
        
        # Overlay escuro (fundo)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Fundo do menu
        menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        menu_surface.fill(self.bg_color)
        
        # Borda do menu
        pygame.draw.rect(
            menu_surface,
            self.border_color,
            (0, 0, self.menu_width, self.menu_height),
            3
        )
        
        # Título
        title_text = self.font_title.render("CARTAS EQUIPADAS", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(self.menu_width // 2, 40))
        menu_surface.blit(title_text, title_rect)
        
        # Contador de slots
        slots_text = self.font_small.render(
            f"{len(player.equipped_cards)}/{player.max_card_slots} slots",
            True,
            COLOR_GRAY
        )
        slots_rect = slots_text.get_rect(center=(self.menu_width // 2, 75))
        menu_surface.blit(slots_text, slots_rect)
        
        # Renderizar slots de cartas
        y_offset = 110
        
        for i in range(player.max_card_slots):
            slot_y = y_offset + (i * (self.slot_height + self.slot_spacing))
            
            # Verificar se tem carta neste slot
            if i < len(player.equipped_cards):
                card = player.equipped_cards[i]
                self._render_card_slot(
                    menu_surface,
                    card,
                    20,
                    slot_y,
                    self.menu_width - 40,
                    self.slot_height,
                    selected=(i == self.selected_slot)
                )
            else:
                # Slot vazio
                self._render_empty_slot(
                    menu_surface,
                    20,
                    slot_y,
                    self.menu_width - 40,
                    self.slot_height
                )
        
        # Instruções
        instructions_y = self.menu_height - 60
        
        instructions = [
            "↑↓ Navegar  |  R: Remover  |  TAB: Fechar"
        ]
        
        for i, text in enumerate(instructions):
            instruction_text = self.font_small.render(text, True, COLOR_GRAY)
            instruction_rect = instruction_text.get_rect(
                center=(self.menu_width // 2, instructions_y + (i * 25))
            )
            menu_surface.blit(instruction_text, instruction_rect)
        
        # Mensagem de confirmação de remoção
        if self.confirming_removal:
            confirm_text = self.font_medium.render(
                "Pressione R novamente para CONFIRMAR",
                True,
                COLOR_RED
            )
            confirm_rect = confirm_text.get_rect(center=(self.menu_width // 2, instructions_y - 30))
            
            # Fundo da mensagem
            bg_rect = confirm_rect.inflate(20, 10)
            pygame.draw.rect(menu_surface, (50, 0, 0, 200), bg_rect)
            pygame.draw.rect(menu_surface, COLOR_RED, bg_rect, 2)
            
            menu_surface.blit(confirm_text, confirm_rect)
        
        # Blit menu na tela
        screen.blit(menu_surface, (self.menu_x, self.menu_y))
    
    def _render_card_slot(self, surface, card, x, y, width, height, selected=False):
        """
        Renderiza um slot com carta
        
        Args:
            surface: Surface para renderizar
            card: Card object
            x, y: Posição
            width, height: Dimensões
            selected: Se está selecionado
        """
        # Cor da raridade
        rarity_color = card.get_rarity_color()
        
        # Fundo do slot
        slot_color = (40, 40, 50, 255) if not selected else (60, 60, 80, 255)
        pygame.draw.rect(surface, slot_color, (x, y, width, height))
        
        # Borda (cor da raridade se selecionado, cinza se não)
        border_color = self.selected_color if selected else rarity_color
        border_width = 3 if selected else 2
        pygame.draw.rect(surface, border_color, (x, y, width, height), border_width)
        
        # Ícone da carta (quadrado colorido)
        icon_size = 80
        icon_x = x + 15
        icon_y = y + (height - icon_size) // 2
        
        # Fundo do ícone
        pygame.draw.rect(surface, (20, 20, 20), (icon_x, icon_y, icon_size, icon_size))
        
        # Borda do ícone (cor da raridade)
        pygame.draw.rect(surface, rarity_color, (icon_x, icon_y, icon_size, icon_size), 3)
        
        # Símbolo no ícone
        icon_center_x = icon_x + icon_size // 2
        icon_center_y = icon_y + icon_size // 2
        
        if card.type == 'passive':
            pygame.draw.circle(surface, rarity_color, (icon_center_x, icon_center_y), 20)
        elif card.type == 'active':
            # Estrela simples
            pygame.draw.polygon(
                surface,
                rarity_color,
                [
                    (icon_center_x, icon_center_y - 20),
                    (icon_center_x + 8, icon_center_y - 5),
                    (icon_center_x + 20, icon_center_y),
                    (icon_center_x + 8, icon_center_y + 8),
                    (icon_center_x, icon_center_y + 20),
                    (icon_center_x - 8, icon_center_y + 8),
                    (icon_center_x - 20, icon_center_y),
                    (icon_center_x - 8, icon_center_y - 5),
                ]
            )
        
        # Nome da carta
        name_x = icon_x + icon_size + 15
        name_y = y + 15
        
        name_text = self.font_large.render(card.name, True, rarity_color)
        surface.blit(name_text, (name_x, name_y))
        
        # Raridade
        rarity_text = self.font_small.render(
            card.rarity.upper(),
            True,
            rarity_color
        )
        surface.blit(rarity_text, (name_x, name_y + 35))
        
        # Descrição
        desc_y = name_y + 60
        desc_text = self.font_small.render(card.description, True, COLOR_GRAY)
        surface.blit(desc_text, (name_x, desc_y))
    
    def _render_empty_slot(self, surface, x, y, width, height):
        """
        Renderiza um slot vazio
        
        Args:
            surface: Surface para renderizar
            x, y: Posição
            width, height: Dimensões
        """
        # Fundo do slot (mais escuro)
        pygame.draw.rect(surface, (30, 30, 35, 255), (x, y, width, height))
        
        # Borda pontilhada (simulada)
        border_color = (80, 80, 90)
        pygame.draw.rect(surface, border_color, (x, y, width, height), 2)
        
        # Texto "VAZIO"
        empty_text = self.font_medium.render("[ VAZIO ]", True, (100, 100, 110))
        empty_rect = empty_text.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(empty_text, empty_rect)
    
    def should_handle_card_pickup(self, player, card):
        """
        Verifica se deve abrir menu ao pegar carta com slots cheios
        
        Args:
            player: Player object
            card: Card que está tentando pegar
            
        Returns:
            bool: True se deve abrir menu de troca
        """
        if len(player.equipped_cards) >= player.max_card_slots:
            print(f"⚠️ Slots cheios! Abrir menu para trocar carta...")
            self.open()
            return True
        return False