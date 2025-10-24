"""
Plane Free - Main Entry Point
Um shoot 'em up roguelike espacial

Sprint 1: Core Gameplay - Movimento, Tiro, Input, Background
"""

import pygame
import sys
from constants import *
from config import config
from src.states.game_state import GameState


class Game:
    """Classe principal do jogo"""
    
    def __init__(self):
        """Inicializa o jogo"""
        # Inicializar Pygame
        pygame.init()
        
        # Criar janela
        if config.fullscreen:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        
        # Configurar janela
        pygame.display.set_caption(f"{GAME_TITLE} v{GAME_VERSION}")
        
        # Clock para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.running = True
        self.dt = 0
        
        # Estado de gameplay
        self.game_state = GameState(self.screen)
        
        print(f"✓ {GAME_TITLE} inicializado!")
        print(f"✓ Pygame versão: {pygame.version.ver}")
        print(f"✓ Resolução: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"✓ FPS alvo: {FPS}")
    
    def handle_events(self):
        """Processa eventos de input"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # ESC para sair
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # H para toggle hitbox (debug)
                if event.key == pygame.K_h:
                    config.show_hitboxes = not config.show_hitboxes
                    print(f"Show Hitboxes: {config.show_hitboxes}")
                
                # F para toggle FPS
                if event.key == pygame.K_f:
                    config.show_fps = not config.show_fps
                    print(f"Show FPS: {config.show_fps}")
                
                # K para kill player (teste game over)
                if event.key == pygame.K_k:
                    self.game_state.player.take_damage(999)
                    print("Player killed (test)")
        
        # Passar eventos para o game state
        self.game_state.handle_events(events)
    
    def update(self):
        """Atualiza lógica do jogo"""
        self.game_state.update(self.dt)
    
    def render(self):
        """Renderiza o jogo na tela"""
        # GameState renderiza tudo
        self.game_state.render()
        
        # Atualizar display
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        print("\n" + "="*50)
        print(f"  {GAME_TITLE} v{GAME_VERSION}")
        print(f"  Sprint 1: Core Gameplay COMPLETO")
        print("="*50)
        print()
        print("CONTROLES:")
        print("  WASD/Setas/Analógico: Mover")
        print("  Tiro: Automático")
        print("  TAB: Pausar")
        print()
        print("DEBUG/TESTE:")
        print("  1/2/3/4: Velocidade do Starfield (0.5x/1x/2x/3x)")
        print("  -/+: Densidade de Estrelas (50-500)")
        print("  H: Toggle Hitbox")
        print("  F: Toggle FPS")
        print("  K: Kill Player (testar Game Over)")
        print()
        print("  ESC: Sair")
        print()
        print("Iniciando loop principal...")
        print()
        
        while self.running:
            # Delta time (em segundos)
            self.dt = self.clock.tick(FPS) / 1000.0
            
            # Processar eventos
            self.handle_events()
            
            # Atualizar
            self.update()
            
            # Renderizar
            self.render()
        
        # Cleanup
        self.quit()
    
    def quit(self):
        """Encerra o jogo"""
        print("\n" + "="*50)
        print("  Encerrando Plane Free")
        print("  Obrigado por jogar!")
        print("="*50)
        pygame.quit()
        sys.exit()


def main():
    """Função principal"""
    # Criar e executar jogo
    game = Game()
    game.run()


if __name__ == "__main__":
    main()