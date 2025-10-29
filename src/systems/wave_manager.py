"""
WaveManager - Gerenciador de setores, spawns e progressão
SISTEMA SIMPLIFICADO: Apenas SETORES (sem waves)
"""

import random
import pygame
from constants import *
from src.entities.enemy_kamikaze import EnemyKamikaze
from src.entities.enemy_range import EnemyRange
from src.entities.enemy_mother import EnemyMother


class WaveManager:
    """Gerencia setores, spawns e progressão"""
    
    def __init__(self):
        """Inicializa o wave manager"""
        # Progressão
        self.current_sector = 1
        
        # Estado do setor
        self.sector_active = False
        self.sector_complete = False
        
        # Countdown entre setores
        self.sector_countdown = 0
        self.sector_countdown_duration = 5.0
        
        # Spawning contínuo
        self.spawn_timer = 0
        self.spawn_interval = 1.2  # Spawn a cada 1.2s
        self.enemies_to_spawn = 0
        self.enemies_spawned = 0
        self.spawn_batch_size = 3  # Spawna 3 por vez
        
        # Miniboss
        self.miniboss_active = False
        self.miniboss_chance = 0.25  # 25%
        
        # Pools
        self.kamikaze_pool = []
        self.range_pool = []
        self.mother_pool = []
        
        self._create_pools()
        self.start_sector()
        
        print(f"✅ WaveManager inicializado - Setor {self.current_sector}")
    
    def _create_pools(self):
        """Cria pools de inimigos"""
        for _ in range(60):
            k = EnemyKamikaze()
            self.kamikaze_pool.append(k)
        
        for _ in range(30):
            r = EnemyRange()
            self.range_pool.append(r)
        
        # ✅ NOVO: Pool de Mães
        for _ in range(10):
            m = EnemyMother()
            self.mother_pool.append(m)
        
        print(f"✅ Pools criados: {len(self.kamikaze_pool)} Kamikazes, {len(self.range_pool)} Ranges, {len(self.mother_pool)} Mães")
    
    def get_kamikaze(self):
        """Pega Kamikaze do pool"""
        for k in self.kamikaze_pool:
            if not k.active:
                return k
        k = EnemyKamikaze()
        self.kamikaze_pool.append(k)
        return k
    
    def get_range(self):
        """Pega Range do pool"""
        for r in self.range_pool:
            if not r.active:
                return r
        r = EnemyRange()
        self.range_pool.append(r)
        return r
    
    def start_sector(self):
        """Inicia novo setor"""
        self.sector_active = True
        self.sector_complete = False
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.miniboss_active = False
        
        # Calcular inimigos do setor
        self.enemies_to_spawn = self._calculate_enemy_count()
        
        # Ajustar batch size
        if self.enemies_to_spawn <= 15:
            self.spawn_batch_size = 2
        elif self.enemies_to_spawn <= 30:
            self.spawn_batch_size = 3
        else:
            self.spawn_batch_size = 4
        
        print(f"\n🚀 SETOR {self.current_sector} INICIADO - {self.enemies_to_spawn} inimigos (grupos de {self.spawn_batch_size})")
    
    def _calculate_enemy_count(self):
        """Calcula inimigos do setor"""
        # Progressão: Setor 1 = 20, Setor 2 = 25, Setor 3 = 30...
        base = 15
        sector_bonus = (self.current_sector - 1) * 5
        total = base + sector_bonus
        return min(total, 100)  # Cap de 100 inimigos por setor
    
    def update(self, dt, active_enemies):
        """Atualiza o manager"""
        # Countdown entre setores
        if self.sector_countdown > 0:
            self.sector_countdown -= dt
            if self.sector_countdown <= 0:
                self.start_sector()
            return
        
        if not self.sector_active:
            return
        
        # Spawnar inimigos continuamente
        if self.enemies_spawned < self.enemies_to_spawn:
            self.spawn_timer += dt
            
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self._spawn_batch()
        
        # Verificar se setor terminou
        if self.enemies_spawned >= self.enemies_to_spawn:
            if len(active_enemies) == 0:
                self._complete_sector()
    
    def get_mother(self):
        """Pega Mãe do pool"""
        for m in self.mother_pool:
            if not m.active:
                return m
        m = EnemyMother()
        self.mother_pool.append(m)
        return m
    
    def _spawn_batch(self):
        """Spawna grupo de inimigos"""
        remaining = self.enemies_to_spawn - self.enemies_spawned
        batch_size = min(self.spawn_batch_size, remaining)
        
        for i in range(batch_size):
            enemy_type = self._choose_enemy_type()
            
            # Posição ESPALHADA
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = -50 - random.randint(0, 100)
            
            if enemy_type == 'kamikaze':
                enemy = self.get_kamikaze()
                ai_level = self._get_ai_level()
                enemy.set_ai_level(ai_level)
                enemy.spawn(x, y)
                self._apply_sector_stats(enemy)
            
            elif enemy_type == 'range':
                enemy = self.get_range()
                ai_level = self._get_ai_level()
                enemy.set_ai_level(ai_level)
                enemy.spawn(x, y)
                self._apply_sector_stats(enemy)
            
            # ✅ NOVO: Mother
            elif enemy_type == 'mother':
                enemy = self.get_mother()
                ai_level = self._get_ai_level()
                enemy.set_ai_level(ai_level)
                enemy.spawn(x, y)
                self._apply_sector_stats(enemy)
            
            self.enemies_spawned += 1
        
        if self.enemies_spawned % 10 == 0 or self.enemies_spawned == self.enemies_to_spawn:
            print(f"  📍 Spawned: {self.enemies_spawned}/{self.enemies_to_spawn}")
    
    def _apply_sector_stats(self, enemy):
        """Aplica stats baseados no setor atual"""
        # ✅ Escalada mais suave
        hp_mult = 1 + (self.current_sector * 0.10)  # Era 0.15
        speed_mult = 1 + (self.current_sector * 0.05)  # Era 0.08
        damage_mult = 1 + (self.current_sector * 0.08)  # Era 0.10
        
        # Caps para evitar valores absurdos
        hp_mult = min(hp_mult, 3.0)  # Max 3x HP
        speed_mult = min(speed_mult, 2.0)  # Max 2x velocidade
        damage_mult = min(damage_mult, 2.5)  # Max 2.5x dano
        
        # Aplicar
        enemy.max_hp = int(enemy.max_hp * hp_mult)
        enemy.hp = enemy.max_hp
        enemy.speed = int(enemy.speed * speed_mult)
        enemy.damage = int(enemy.damage * damage_mult)
        
        # Value baseado no tipo
        if enemy.enemy_type == 'kamikaze':
            enemy.value = 10  # ✅ Sempre 10 (1 minério)
        elif enemy.enemy_type == 'range':
            enemy.value = 20  # ✅ Sempre 20 (2 minérios)
        elif enemy.enemy_type == 'mother':
            enemy.value = 50  # ✅ Sempre 50 (5 minérios)
    
    def _choose_enemy_type(self):
        """Escolhe tipo de inimigo"""
        if self.current_sector == 1:
            return 'kamikaze'
        elif self.current_sector == 2:
            return 'kamikaze' if random.random() < 0.80 else 'range'
        elif self.current_sector >= 3:
            # ✅ 65% Kamikaze, 32% Range, 3% Mother
            rand = random.random()
            if rand < 0.65:
                return 'kamikaze'
            elif rand < 0.97:
                return 'range'
            else:
                return 'mother'
    
    def _get_ai_level(self):
        """Determina AI level baseado no setor"""
        # A cada 7 setores, aumenta 1 nível de IA
        return min((self.current_sector - 1) // 7, 6)
    
    def _complete_sector(self):
        """Completa o setor"""
        self.sector_active = False
        self.sector_complete = True
        
        print(f"\n🎉 SETOR {self.current_sector} COMPLETO!")
        
        # 25% chance de miniboss
        if not self._is_boss_sector() and random.random() < self.miniboss_chance:
            print("⚠️ MINIBOSS APARECENDO!")
            self.miniboss_active = True
            # TODO: Spawnar miniboss
        
        # Próximo setor
        self.current_sector += 1
        
        # Boss a cada 7 setores
        if self._is_boss_sector():
            print(f"💀 BOSS NO SETOR {self.current_sector}!")
            # TODO: Spawnar boss
        
        # Countdown
        self.sector_countdown = self.sector_countdown_duration
        print(f"⏳ Countdown: {self.sector_countdown_duration:.0f}s até SETOR {self.current_sector}...")
    
    def _is_boss_sector(self):
        """Verifica se é setor de boss"""
        return self.current_sector % 7 == 0
    
    def get_active_enemies(self):
        """Retorna inimigos ativos"""
        active = []
        for k in self.kamikaze_pool:
            if k.active:
                active.append(k)
        for r in self.range_pool:
            if r.active:
                active.append(r)
        for m in self.mother_pool:
            if m.active:
                active.append(m)
        return active
    
    def get_countdown_text(self):
        """Retorna texto do countdown"""
        if self.sector_countdown <= 0:
            return None
        
        seconds = int(self.sector_countdown) + 1
        
        if seconds > 1:
            return f"SETOR {self.current_sector}\n{seconds}"
        else:
            return "GO!"