"""
Object Pool - Sistema de pooling de objetos para otimização
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class ObjectPool:
    """Pool genérico de objetos"""
    
    def __init__(self, object_class, initial_size=50):
        """
        Inicializa o pool
        
        Args:
            object_class: Classe dos objetos a serem poolados
            initial_size (int): Quantidade inicial de objetos
        """
        self.object_class = object_class
        self.available = []
        self.in_use = []
        
        # Pré-popular pool
        for _ in range(initial_size):
            obj = object_class()
            obj.active = False
            self.available.append(obj)
    
    def get(self):
        """
        Pega um objeto do pool
        
        Returns:
            object: Objeto disponível ou novo se pool vazio
        """
        if self.available:
            obj = self.available.pop()
            self.in_use.append(obj)
            return obj
        else:
            # Pool esgotado, criar novo
            obj = self.object_class()
            self.in_use.append(obj)
            return obj
    
    def return_object(self, obj):
        """
        Retorna objeto ao pool
        
        Args:
            obj: Objeto a ser retornado
        """
        if obj in self.in_use:
            obj.active = False
            self.in_use.remove(obj)
            self.available.append(obj)
    
    def update_all(self, dt):
        """
        Atualiza todos os objetos em uso
        
        Args:
            dt (float): Delta time
        """
        for obj in self.in_use[:]:  # Copia lista para evitar problemas
            obj.update(dt)
            
            # Se desativado, retorna ao pool
            if not obj.active:
                self.return_object(obj)
    
    def render_all(self, screen):
        """
        Renderiza todos os objetos ativos
        
        Args:
            screen: Pygame surface
        """
        for obj in self.in_use:
            if obj.active:
                obj.render(screen)
    
    def get_active_count(self):
        """Retorna quantidade de objetos ativos"""
        return len(self.in_use)
    
    def get_available_count(self):
        """Retorna quantidade de objetos disponíveis"""
        return len(self.available)
    
    def clear_all(self):
        """Remove todos os objetos ativos"""
        for obj in self.in_use[:]:
            obj.active = False
            self.return_object(obj)