"""
Configurações carregáveis do jogo
"""

class Config:
    """Configurações do jogo"""
    
    def __init__(self):
        # Vídeo
        self.fullscreen = False
        self.vsync = True
        self.show_fps = True  # Debug
        
        # Áudio
        self.master_volume = 0.8
        self.music_volume = 0.6
        self.sfx_volume = 0.9
        
        # Debug
        self.debug_mode = True
        self.show_hitboxes = False
        
    def load(self):
        """Carrega configurações de arquivo (implementar depois)"""
        pass
    
    def save(self):
        """Salva configurações em arquivo (implementar depois)"""
        pass

# Instância global
config = Config()