"""
Card - Carta equipável que modifica stats do player
"""

import json
import os


class Card:
    """Classe de carta equipável"""
    
    def __init__(self, card_data):
        """
        Inicializa carta
        
        Args:
            card_data (dict): Dados da carta do JSON
        """
        self.id = card_data['id']
        self.name = card_data['name']
        self.rarity = card_data['rarity']  # comum, incomum, epico
        self.type = card_data['type']  # passive, active
        self.description = card_data['description']
        self.effect = card_data['effect']
    
    def apply_effect(self, player):
        """
        Aplica efeito da carta no player
        
        Args:
            player: Objeto Player
        """
        stat = self.effect['stat']
        operation = self.effect['operation']
        value = self.effect['value']
        
        if operation == 'add':
            # Somar valor
            current = getattr(player, stat, 0)
            setattr(player, stat, current + value)
            print(f"✨ {self.name}: {stat} +{value} = {current + value}")
        
        elif operation == 'multiply':
            # Multiplicar valor
            current = getattr(player, stat, 1)
            new_value = current * value
            setattr(player, stat, new_value)
            print(f"✨ {self.name}: {stat} ×{value} = {new_value:.2f}")
        
        elif operation == 'set':
            # Definir valor
            setattr(player, stat, value)
            print(f"✨ {self.name}: {stat} = {value}")
    
    def remove_effect(self, player):
        """
        Remove efeito da carta do player
        
        Args:
            player: Objeto Player
        """
        stat = self.effect['stat']
        operation = self.effect['operation']
        value = self.effect['value']
        
        if operation == 'add':
            # Subtrair valor
            current = getattr(player, stat, 0)
            setattr(player, stat, current - value)
        
        elif operation == 'multiply':
            # Dividir valor
            current = getattr(player, stat, 1)
            setattr(player, stat, current / value)
        
        elif operation == 'set':
            # Resetar para padrão (não podemos reverter set facilmente)
            pass
    
    def get_rarity_color(self):
        """Retorna cor baseada na raridade"""
        if self.rarity == 'comum':
            return (200, 200, 200)  # Cinza
        elif self.rarity == 'incomum':
            return (100, 150, 255)  # Azul
        elif self.rarity == 'epico':
            return (200, 0, 255)    # Roxo
        else:
            return (255, 255, 255)  # Branco


class CardManager:
    """Gerenciador de cartas"""
    
    def __init__(self):
        """Inicializa o card manager"""
        self.all_cards = []
        self.load_cards()
    
    def load_cards(self):
        """Carrega cartas do JSON"""
        json_path = os.path.join('data', 'cards.json')
        
        if not os.path.exists(json_path):
            print(f"❌ ERRO: {json_path} não encontrado!")
            return
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for card_data in data['cards']:
                card = Card(card_data)
                self.all_cards.append(card)
        
        print(f"✅ {len(self.all_cards)} cartas carregadas")
    
    def get_card_by_id(self, card_id):
        """
        Busca carta por ID
        
        Args:
            card_id (str): ID da carta
            
        Returns:
            Card ou None
        """
        for card in self.all_cards:
            if card.id == card_id:
                return card
        return None
    
    def get_random_card(self, rarity=None):
        """
        Retorna carta aleatória
        
        Args:
            rarity (str): Filtrar por raridade (opcional)
            
        Returns:
            Card
        """
        import random
        
        if rarity:
            filtered = [c for c in self.all_cards if c.rarity == rarity]
            if filtered:
                return random.choice(filtered)
        
        return random.choice(self.all_cards)
    
    def roll_rarity(self):
        """
        Rola raridade baseado em chances
        
        Returns:
            str: 'comum', 'incomum' ou 'epico'
        """
        import random
        
        # 80% comum, 19% incomum, 1% épico
        rand = random.random()
        
        if rand < 0.80:
            return 'comum'
        elif rand < 0.99:
            return 'incomum'
        else:
            return 'epico'