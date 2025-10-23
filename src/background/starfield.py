"""
Starfield - Campo de estrelas animado
"""

import pygame
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from constants import *


class Star:
    """Uma estrela individual"""
    
    def __init__(self, x, y, size, speed, brightness):
        """
        Inicializa uma estrela
        
        Args:
            x (float): Posição X
            y (float): Posição Y
            size (int): Tamanho (1-3 pixels)
            speed (float): Velocidade de descida
            brightness (int): Brilho (0-255)
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.brightness = brightness
        self.color = (brightness, brightness, brightness)
    
    def update(self, dt, scroll_speed_multiplier=1.0):
        """
        Atualiza posição da estrela
        
        Args:
            dt (float): Delta time
            scroll_speed_multiplier (float): Multiplicador de velocidade
        """
        self.y += self.speed * scroll_speed_multiplier * dt
        
        # Se sair da tela, reposicionar no topo
        if self.y > SCREEN_HEIGHT + 10:
            self.y = -10
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def render(self, screen):
        """Renderiza a estrela"""
        if self.size == 1:
            # Estrela pequena (1 pixel)
            screen.set_at((int(self.x), int(self.y)), self.color)
        else:
            # Estrela maior (círculo)
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                self.size
            )


class Starfield:
    """Campo de estrelas com múltiplas camadas"""
    
    def __init__(self, star_count=200):
        """
        Inicializa o starfield
        
        Args:
            star_count (int): Quantidade total de estrelas
        """
        self.stars = []
        self.star_count = star_count
        self.scroll_speed_multiplier = 1.0
        
        # Criar estrelas
        self.generate_stars()
    
    def generate_stars(self):
        """Gera estrelas com diferentes camadas de profundidade"""
        self.stars = []
        
        for i in range(self.star_count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            
            # Probabilidade de diferentes tipos
            rand = random.random()
            
            if rand < 0.60:  # 60% - Estrelas distantes (lentas, pequenas, escuras)
                size = 1
                speed = random.randint(20, 40)
                brightness = random.randint(80, 120)
            
            elif rand < 0.85:  # 25% - Estrelas médias
                size = random.choice([1, 2])
                speed = random.randint(40, 80)
                brightness = random.randint(120, 180)
            
            else:  # 15% - Estrelas próximas (rápidas, grandes, brilhantes)
                size = random.choice([2, 3])
                speed = random.randint(80, 150)
                brightness = random.randint(180, 255)
            
            star = Star(x, y, size, speed, brightness)
            self.stars.append(star)
    
    def update(self, dt):
        """
        Atualiza todas as estrelas
        
        Args:
            dt (float): Delta time
        """
        for star in self.stars:
            star.update(dt, self.scroll_speed_multiplier)
    
    def render(self, screen):
        """
        Renderiza todas as estrelas
        
        Args:
            screen: Pygame surface
        """
        for star in self.stars:
            star.render(screen)
    
    def set_scroll_speed(self, multiplier):
        """
        Ajusta velocidade de scroll
        
        Args:
            multiplier (float): Multiplicador (1.0 = normal, 2.0 = 2x mais rápido)
        """
        self.scroll_speed_multiplier = multiplier
    
    def set_density(self, star_count):
        """
        Ajusta densidade de estrelas
        
        Args:
            star_count (int): Nova quantidade de estrelas
        """
        self.star_count = star_count
        self.generate_stars()


class Background:
    """Gerenciador de background completo"""
    
    def __init__(self):
        """Inicializa o background"""
        # Cor de fundo base
        self.bg_color = COLOR_BLACK
        
        # Starfield
        self.starfield = Starfield(star_count=200)
        
        # Efeitos adicionais (para depois)
        self.effects = []
    
    def update(self, dt):
        """
        Atualiza background
        
        Args:
            dt (float): Delta time
        """
        self.starfield.update(dt)
    
    def render(self, screen):
        """
        Renderiza background
        
        Args:
            screen: Pygame surface
        """
        # Limpar com cor base
        screen.fill(self.bg_color)
        
        # Renderizar starfield
        self.starfield.render(screen)
    
    def set_atmosphere(self, atmosphere_name):
        """
        Muda atmosfera (para implementar depois)
        
        Args:
            atmosphere_name (str): Nome da atmosfera
        """
        # TODO: Implementar mudança de atmosfera
        pass