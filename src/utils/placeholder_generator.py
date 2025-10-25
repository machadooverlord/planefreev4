"""
Gerador de sprites placeholder para desenvolvimento
"""

import sys
import os

# Adiciona a pasta raiz ao path (para imports funcionarem)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pygame
from constants import *


def create_player_sprite(size=32):
    """Cria sprite placeholder do player (triângulo azul)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Triângulo apontando para cima
    points = [
        (size // 2, 0),           # Topo
        (0, size),                # Inferior esquerdo
        (size, size)              # Inferior direito
    ]
    
    pygame.draw.polygon(surface, COLOR_BLUE, points)
    pygame.draw.polygon(surface, COLOR_WHITE, points, 2)  # Borda
    
    return surface


def create_enemy_sprite(size=24, color=COLOR_RED):
    """Cria sprite placeholder de inimigo (quadrado)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    pygame.draw.rect(surface, color, (0, 0, size, size))
    pygame.draw.rect(surface, COLOR_WHITE, (0, 0, size, size), 2)  # Borda
    
    return surface


def create_projectile_sprite(width=6, height=12, color=COLOR_YELLOW):
    """Cria sprite placeholder de projétil (retângulo)"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    pygame.draw.rect(surface, color, (0, 0, width, height))
    
    return surface


def create_collectible_sprite(size=12):
    """Cria sprite placeholder de minério (círculo)"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    center = size // 2
    pygame.draw.circle(surface, (0, 255, 255), (center, center), center)
    pygame.draw.circle(surface, COLOR_WHITE, (center, center), center, 2)
    
    return surface


if __name__ == "__main__":
    """Testa a geração de sprites"""
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Placeholder Sprites Test")
    
    player = create_player_sprite()
    enemy = create_enemy_sprite()
    projectile = create_projectile_sprite()
    collectible = create_collectible_sprite()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill(COLOR_BLACK)
        
        # Mostrar sprites
        screen.blit(player, (100, 100))
        screen.blit(enemy, (200, 100))
        screen.blit(projectile, (100, 200))
        screen.blit(collectible, (200, 200))
        
        # Labels
        font = pygame.font.Font(None, 24)
        labels = [
            (font.render("Player", True, COLOR_WHITE), (90, 140)),
            (font.render("Enemy", True, COLOR_WHITE), (190, 140)),
            (font.render("Projectile", True, COLOR_WHITE), (70, 220)),
            (font.render("Collectible", True, COLOR_WHITE), (170, 220)),
        ]
        for text, pos in labels:
            screen.blit(text, pos)
        
        pygame.display.flip()
    
    pygame.quit()