"""
Input Manager - Gerenciador de inputs (teclado e gamepad)
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class InputManager:
    """Gerencia inputs de teclado e gamepads"""
    
    def __init__(self):
        """Inicializa o input manager"""
        # Joysticks/Gamepads
        pygame.joystick.init()
        self.joysticks = []
        self.detect_joysticks()
        
        # Estado atual
        self.keys = None
        
        # Mapeamento de botões (Xbox layout como padrão)
        self.button_map = {
            'A': 0,      # A / X (PlayStation)
            'B': 1,      # B / Circle
            'X': 2,      # X / Square
            'Y': 3,      # Y / Triangle
            'LB': 4,     # Left Bumper / L1
            'RB': 5,     # Right Bumper / R1
            'BACK': 6,   # Back / Select
            'START': 7,  # Start
            'LS': 8,     # Left Stick Click / L3
            'RS': 9,     # Right Stick Click / R3
        }
        
        # Deadzone para analógicos
        self.deadzone = 0.15
    
    def detect_joysticks(self):
        """Detecta e inicializa joysticks/gamepads"""
        joystick_count = pygame.joystick.get_count()
        
        self.joysticks = []
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)
            print(f"✓ Gamepad {i} detectado: {joystick.get_name()}")
        
        if joystick_count == 0:
            print("✓ Nenhum gamepad detectado (usando teclado)")
        
        return joystick_count
    
    def update(self):
        """Atualiza estado dos inputs"""
        # Atualizar teclas
        self.keys = pygame.key.get_pressed()
    
    def get_movement(self, player_index=0):
        """
        Obtém movimento para um jogador específico
        
        Args:
            player_index (int): Índice do jogador (0-3)
            
        Returns:
            tuple: (move_x, move_y) normalizado entre -1 e 1
        """
        move_x = 0
        move_y = 0
        
        # Player 1 sempre usa teclado (ou gamepad 0 se preferir)
        if player_index == 0:
            # Teclado (WASD ou Setas)
            if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
                move_x -= 1
            if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
                move_x += 1
            if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
                move_y -= 1
            if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
                move_y += 1
            
            # Se tiver gamepad 0, pode usar também
            if len(self.joysticks) > 0:
                axis_x = self.joysticks[0].get_axis(0)  # Left stick X
                axis_y = self.joysticks[0].get_axis(1)  # Left stick Y
                
                # Aplicar deadzone
                if abs(axis_x) > self.deadzone:
                    move_x = axis_x
                if abs(axis_y) > self.deadzone:
                    move_y = axis_y
        
        # Players 2-4 usam gamepads 1-3
        elif 1 <= player_index <= 3:
            gamepad_index = player_index  # Player 2 = Gamepad 1, etc
            
            if gamepad_index < len(self.joysticks):
                joystick = self.joysticks[gamepad_index]
                
                # Analógico esquerdo
                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)
                
                # Aplicar deadzone
                if abs(axis_x) > self.deadzone:
                    move_x = axis_x
                if abs(axis_y) > self.deadzone:
                    move_y = axis_y
                
                # D-pad como fallback
                hat = joystick.get_hat(0) if joystick.get_numhats() > 0 else (0, 0)
                if hat[0] != 0:
                    move_x = hat[0]
                if hat[1] != 0:
                    move_y = -hat[1]  # Inverter Y (hat usa +1 para cima)
        
        # Limitar valores entre -1 e 1
        move_x = max(-1, min(1, move_x))
        move_y = max(-1, min(1, move_y))
        
        return move_x, move_y
    
    def get_button(self, button_name, player_index=0):
        """
        Verifica se botão está pressionado
        
        Args:
            button_name (str): Nome do botão ('A', 'B', 'START', etc)
            player_index (int): Índice do jogador
            
        Returns:
            bool: True se pressionado
        """
        # Player 1 pode usar teclado
        if player_index == 0:
            # Mapeamento teclado
            keyboard_map = {
                'A': pygame.K_SPACE,
                'B': pygame.K_LSHIFT,
                'X': pygame.K_x,
                'Y': pygame.K_c,
                'START': pygame.K_RETURN,
                'BACK': pygame.K_TAB,
            }
            
            if button_name in keyboard_map:
                if self.keys[keyboard_map[button_name]]:
                    return True
        
        # Gamepad
        gamepad_index = player_index if player_index > 0 else 0
        
        if gamepad_index < len(self.joysticks):
            joystick = self.joysticks[gamepad_index]
            
            if button_name in self.button_map:
                button_id = self.button_map[button_name]
                
                if button_id < joystick.get_numbuttons():
                    return joystick.get_button(button_id)
        
        return False
    
    def is_key_pressed(self, key):
        """
        Verifica se tecla específica está pressionada
        
        Args:
            key: pygame.K_* constant
            
        Returns:
            bool: True se pressionada
        """
        return self.keys[key]
    
    def get_joystick_count(self):
        """Retorna quantidade de joysticks conectados"""
        return len(self.joysticks)