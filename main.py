"""
Plane Free - Main Entry Point
Um shoot 'em up roguelike espacial

Sprint 0: Setup básico
"""

import pygame
import sys
from constants import *
from config import config


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
        self.dt = 0  # Delta time
        
        print(f"✓ {GAME_TITLE} inicializado!")
        print(f"✓ Pygame versão: {pygame.version.ver}")
        print(f"✓ Resolução: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"✓ FPS alvo: {FPS}")
    
    def handle_events(self):
        """Processa eventos de input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # ESC para sair (temporário)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Atualiza lógica do jogo"""
        # Por enquanto, nada para atualizar
        pass
    
    def render(self):
        """Renderiza o jogo na tela"""
        # Limpar tela (preto)
        self.screen.fill(COLOR_BLACK)
        
        # Texto de teste
        if config.debug_mode:
            font = pygame.font.Font(None, 36)
            
            # Título
            title_text = font.render(
                f"{GAME_TITLE} - Sprint 0",
                True,
                COLOR_WHITE
            )
            title_rect = title_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(title_text, title_rect)
            
            # Instruções
            instruction_text = font.render(
                "Pressione ESC para sair",
                True,
                COLOR_GRAY
            )
            instruction_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            self.screen.blit(instruction_text, instruction_rect)
            
            # FPS
            if config.show_fps:
                fps = int(self.clock.get_fps())
                fps_text = font.render(
                    f"FPS: {fps}",
                    True,
                    COLOR_GREEN if fps >= 55 else COLOR_YELLOW
                )
                self.screen.blit(fps_text, (10, 10))
        
        # Atualizar display
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        print("\n=== Iniciando loop principal ===\n")
        
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
        print("\n=== Encerrando jogo ===")
        pygame.quit()
        sys.exit()


def main():
    """Função principal"""
    print("="*50)
    print(f"  {GAME_TITLE} v{GAME_VERSION}")
    print("  Sprint 0: Setup e Preparação")
    print("="*50)
    print()
    
    # Criar e executar jogo
    game = Game()
    game.run()


if __name__ == "__main__":
    main()