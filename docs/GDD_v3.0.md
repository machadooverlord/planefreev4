Todo o Gdd foi colocado em uma pasta externa ao github para que não ocupe muito espaço, mas permiti os APÊNDICES ficarem aqui.

14. APÊNDICES

APÊNDICES
APÊNDICE A: Template JSON - Cartas
json{
  "id": "otimizacao_mira",
  "name": "Otimização de Mira",
  "rarity": "comum",
  "type": "passiva",
  "description": "Dano de Projétil +{valor}%",
  "effect": {
    "stat": "projectile_damage",
    "operation": "multiply",
    "values": [1.20, 1.30, 1.40, 1.50, 1.60]
  },
  "max_level": 5,
  "fusion_requirements": {
    "level_2": {"copies": 2, "minerals": 0, "cards": []},
    "level_3": {"copies": 3, "minerals": 500, "cards": []},
    "level_4": {"copies": 4, "minerals": 1500, "cards": ["any_uncommon"]},
    "level_5": {"copies": 5, "minerals": 3000, "cards": ["any_epic"]}
  },
  "synergies": [
    {
      "with": ["sensor_varredura"],
      "effect": "critico_damage_bonus",
      "value": 0.15,
      "description": "Críticos causam +15% dano adicional"
    }
  ],
  "icon": "assets/cards/otimizacao_mira.png",
  "unlock_requirement": null
}

APÊNDICE B: Template JSON - Naves
json{
  "id": "tanque_fortaleza",
  "name": "Fortaleza",
  "tier": "T3",
  "class": "tanque",
  "parent": "tanque_base",
  "stats": {
    "hp": 250,
    "speed": 180,
    "fire_rate": 0.45,
    "damage": 18,
    "card_slots": 4
  },
  "special_ability": {
    "name": "Escudo Frontal Passivo",
    "description": "Absorve 30% do dano recebido pela frente",
    "cooldown": null,
    "type": "passive"
  },
  "rotation_mode": "fixed",
  "sprites": {
    "base": "assets/ships/fortaleza_0.png",
    "evolutions": [
      "assets/ships/fortaleza_1.png",
      "assets/ships/fortaleza_2.png",
      "assets/ships/fortaleza_3.png",
      "assets/ships/fortaleza_4.png",
      "assets/ships/fortaleza_5.png",
      "assets/ships/fortaleza_6.png",
      "assets/ships/fortaleza_7.png"
    ]
  },
  "unlock_requirement": {
    "type": "boss_defeat",
    "boss_id": "guardian_mk2",
    "sector": 14
  }
}

APÊNDICE C: Template JSON - Inimigos
json{
  "id": "kamikaze",
  "name": "Kamikaze",
  "type": "kamikaze",
  "base_stats": {
    "hp": 30,
    "speed": 150,
    "damage": 20,
    "size": [24, 24]
  },
  "ai_behaviors": [
    {
      "level": 0,
      "sectors": [1, 7],
      "behavior": "straight_down",
      "params": {}
    },
    {
      "level": 1,
      "sectors": [8, 14],
      "behavior": "chase_lateral",
      "params": {"correction_strength": 0.3}
    },
    {
      "level": 2,
      "sectors": [15, 21],
      "behavior": "zigzag",
      "params": {"amplitude": 50, "frequency": 2.0}
    }
  ],
  "drops": {
    "minerals": [10, 15],
    "cards": 0.02,
    "mutated_multiplier": 2.5
  },
  "sprites": {
    "normal": "assets/enemies/kamikaze.png",
    "mutated": "assets/enemies/kamikaze_mutated.png"
  },
  "sounds": {
    "spawn": "sfx/enemy_spawn.wav",
    "death": "sfx/explosion_small.wav"
  }
}

APÊNDICE D: Template JSON - Bosses
json{
  "id": "guardian_mk1",
  "name": "Guardião Mk-I",
  "sector": 7,
  "hp": 1000,
  "size": [128, 128],
  "phases": [
    {
      "phase": 1,
      "hp_range": [100, 70],
      "attacks": [
        {
          "name": "Circular Spread",
          "pattern": "circle",
          "projectiles": 8,
          "cooldown": 2.0,
          "damage": 10
        }
      ],
      "movement": "circular",
      "invulnerable": false
    },
    {
      "phase": 2,
      "hp_range": [70, 30],
      "attacks": [
        {
          "name": "Summon Adds",
          "pattern": "spawn",
          "enemy_type": "kamikaze",
          "count": 3,
          "cooldown": 10.0
        },
        {
          "name": "Laser Sweep",
          "pattern": "laser",
          "duration": 3.0,
          "damage": 15,
          "telegraph": 1.0
        }
      ],
      "movement": "lateral",
      "invulnerable": false
    },
    {
      "phase": 3,
      "hp_range": [30, 0],
      "attacks": [
        {
          "name": "Frenzy Mode",
          "pattern": "bullet_hell",
          "projectiles": 20,
          "cooldown": 1.0,
          "damage": 10
        }
      ],
      "movement": "erratic",
      "invulnerable": false,
      "speed_multiplier": 1.5
    }
  ],
  "drops": {
    "minerals": 300,
    "cards": 1,
    "card_rarity": [0.7, 0.3, 0.0]
  },
  "music": "music/boss_theme_1.ogg",
  "sprites": {
    "phase_1": "assets/bosses/guardian_p1.png",
    "phase_2": "assets/bosses/guardian_p2.png",
    "phase_3": "assets/bosses/guardian_p3.png"
  }
}
```

---

## **APÊNDICE E: Checklist de Sprint**

### **Template para Cada Sprint:**
```
SPRINT X: [Nome do Sprint]
Datas: DD/MM/YYYY - DD/MM/YYYY
Dev Horas Planejadas: 40-60h

OBJETIVOS:
[ ] Objetivo 1
[ ] Objetivo 2
[ ] Objetivo 3

TAREFAS:
[ ] Tarefa 1 (Estimativa: 4h)
[ ] Tarefa 2 (Estimativa: 8h)
[ ] Tarefa 3 (Estimativa: 6h)
...

ENTREGÁVEIS:
[ ] Entregável 1
[ ] Entregável 2

TESTES:
[ ] Teste unitário de [feature]
[ ] Teste de integração
[ ] Playtest manual (30min)

BUGS CONHECIDOS:
- Bug 1: [descrição] (Prioridade: Alta/Média/Baixa)
- Bug 2: [descrição]

NOTAS/DECISÕES:
- Decisão 1: [O que foi decidido e por quê]
- Mudança: [O que mudou do plano original]

RETROSPECTIVA (ao fim):
O que funcionou bem:
-
-

O que melhorar:
-
-

Lições aprendidas:
-
-

STATUS FINAL: ✅ Completo / ⚠️ Parcial / ❌ Atrasado
```

---

## **APÊNDICE F: Checklist de QA (Sprint 36)**

### **Funcionalidade Core:**
```
[ ] Player se move em 8 direções
[ ] Tiro automático funciona
[ ] Colisões funcionam (player, inimigos, projéteis)
[ ] HP system funciona
[ ] Morte funciona
[ ] Game over exibe stats corretas
```

### **Sistema de Waves:**
```
[ ] 7 waves = 1 setor
[ ] Transições suaves
[ ] Countdown funciona
[ ] Spawn rate correto
[ ] Dificuldade escala corretamente até Setor 100
```

### **Inimigos:**
```
[ ] Kamikaze: Todos 7 níveis de IA funcionam
[ ] Range: Todos 7 níveis de IA funcionam
[ ] Mãe: Todos níveis funcionam, filhotes spawnam
[ ] Mutados aparecem com frequência correta
[ ] Drops funcionam (minérios, cartas)
```

### **Bosses:**
```
[ ] Boss 1-14: Todas fases funcionam
[ ] Transições de fase suaves
[ ] HP bars corretas
[ ] Drops corretos
[ ] Música especial toca
```

### **Sistema de Cartas:**
```
[ ] 90 cartas implementadas
[ ] Drop rates corretos (80/19/1%)
[ ] Efeitos aplicam corretamente
[ ] Fusão funciona
[ ] Sinergias detectadas e ativas
[ ] Menu Reajustar funciona
```

### **Sistema de Naves:**
```
[ ] 10 naves implementadas
[ ] Evolução T1→T2→T3 funciona
[ ] Stats corretos por classe
[ ] Rotação funciona (Tanque fixed, Velocista 360°, Técnico 4-dir)
[ ] Mini-evoluções visuais (7 por nave)
[ ] Sprites mudam a cada setor
```

### **Hangar:**
```
[ ] Tab Cartas: Visualização funciona
[ ] Tab Naves: Árvore de evolução clara
[ ] Tab Upgrades: Compras funcionam, persistem
[ ] Tab Customização: Skins/Cores aplicam
[ ] Fusão de cartas funciona
[ ] Progresso salva entre sessões
```

### **Achievements:**
```
[ ] 70 achievements rastreiam corretamente
[ ] Notificações aparecem ao desbloquear
[ ] Recompensas (skins/títulos/cores) desbloqueiam
[ ] Hall de Conquistas mostra progresso
[ ] Persistência funciona
Multiplayer:
[ ] 2-4 jogadores funcionamTentar novamenteLHContinuar[ ] Controles separados (gamepad + teclado)
[ ] Cores distintas por jogador
[ ] HUD mostra todos HP's
[ ] Colisões não interferem entre players
[ ] Spawn rate escala corretamente
[ ] Performance estável (60 FPS)
```

### **Atmosferas:**
```
[ ] 10+ atmosferas implementadas
[ ] Transições suaves (crossfade 3s)
[ ] Parallax funciona em todas
[ ] Densidade de estrelas aumenta gradualmente
[ ] Visual distinto para cada setor
```

### **Eventos e Modificadores:**
```
[ ] 10 eventos aleatórios funcionam (20% chance)
[ ] 10 modificadores de setor funcionam (30% chance)
[ ] Notificações aparecem corretamente
[ ] Efeitos aplicam durante todo setor
[ ] Recompensas extras funcionam
```

### **DDA (Dynamic Difficulty Adjustment):**
```
[ ] Métricas rastreiam corretamente
[ ] Classificação de skill atualiza
[ ] Ajustes aplicam sutilmente
[ ] Limites respeitados (-25% a +40%)
[ ] Pode ser desabilitado no menu
[ ] Debug mode (F3) mostra status
```

### **UI/UX:**
```
[ ] Menu principal navegável
[ ] Menu de pausa funciona
[ ] Tela Game Over completa
[ ] HUD claro e legível
[ ] Tooltips aparecem corretamente
[ ] Transições suaves entre telas
[ ] Sem UI clipping ou overlap
```

### **Performance:**
```
[ ] 60 FPS constante em hardware alvo
[ ] Sem stuttering/lag
[ ] Object pooling funciona
[ ] Spatial partitioning otimiza colisões
[ ] Culling funciona (não renderiza offscreen)
[ ] RAM uso < 500 MB
[ ] Tempo de carregamento < 5s
```

### **Áudio:**
```
[ ] Música toca em todos contextos
[ ] SFX funcionam (tiro, hit, morte, coleta)
[ ] Mixing balanceado
[ ] Sem clipping/distorção
[ ] Opções de volume funcionam
[ ] Música de boss diferenciada
```

### **Save/Load:**
```
[ ] Progresso salva corretamente
[ ] Cartas descobertas persistem
[ ] Upgrades do Hangar persistem
[ ] Achievements persistem
[ ] Leaderboard persiste
[ ] Backup automático funciona
[ ] Corrupção de save recuperável
```

### **Bugs Críticos (Zero Tolerance):**
```
[ ] Sem crashes em gameplay normal
[ ] Sem softlocks (player preso)
[ ] Sem perda de progresso não intencional
[ ] Sem exploits game-breaking
[ ] Sem projéteis atravessando inimigos
[ ] Sem inimigos invencíveis
```

### **Balanceamento:**
```
[ ] Nenhuma carta domina 100% das runs
[ ] Todas 10 naves viáveis até Setor 50
[ ] Dificuldade escala consistentemente
[ ] Bosses desafiadores mas justos
[ ] Setores 1-7 acessíveis para iniciantes
[ ] Setores 80-100 desafiadores para veteranos
```

### **Multiplataforma (Windows/Linux/Mac):**
```
[ ] Builds para todas 3 plataformas
[ ] Controles funcionam em todas
[ ] Sem bugs específicos de plataforma
[ ] Performance equivalente
```

---

## **APÊNDICE G: Glossário de Termos**

### **Termos de Gameplay:**
```
- Wave: Onda de inimigos dentro de um setor (7 waves = 1 setor)
- Setor: Agrupamento de 7 waves, progressão principal
- Tier (T1/T2/T3): Nível evolutivo das naves
- Mini-evolução: Upgrade visual a cada setor (7 por nave)
- Mutado: Inimigo com stats aumentados (15% chance)
- Perfect Wave: Completar wave sem levar dano
- Combo: Sequência de kills sem quebrar (3s timeout)
- AI Level: Nível de inteligência dos inimigos (0-7)
```

### **Termos Técnicos:**
```
- Object Pooling: Reutilização de objetos para performance
- Spatial Partitioning: Divisão de arena em grid para otimizar colisões
- Culling: Não renderizar objetos fora da tela
- I-frames: Invencibilidade temporária pós-hit
- DPS: Damage Per Second (dano por segundo)
- Fire Rate: Taxa de tiro (tiros por segundo)
- Hitbox: Área de colisão do objeto
- Raycast: Linha de visão para detectar colisão de projéteis rápidos
```

### **Termos de Progressão:**
```
- Hangar: Menu principal fora de gameplay
- Fusão: Combinar cartas duplicadas para upgrade
- Ascensão: Cartas ultra-raras desbloqueadas por uso repetido
- Sinergia: Bônus quando duas cartas trabalham juntas
- DDA: Dynamic Difficulty Adjustment (ajuste automático)
- Achievement: Conquista que desbloqueia recompensa
- Skin: Aparência alternativa da nave
- Título: Prefixo no nome do jogador

APÊNDICE H: Fórmulas de Balanceamento
Escala de Stats de Inimigos:
pythondef calculate_enemy_stats(base_hp, base_speed, base_damage, sector):
    if sector <= 100:
        hp_mult = 1 + (sector * 0.15)
        speed_mult = 1 + (sector * 0.08)
        damage_mult = 1 + (sector * 0.10)
        
        # Caps para Setor 100
        hp_mult = min(hp_mult, 16.0)
        speed_mult = min(speed_mult, 9.0)
        damage_mult = min(damage_mult, 11.0)
    else:
        # Escala infinita (101+)
        excess = sector - 100
        hp_mult = 16.0 + (excess * 0.20)
        speed_mult = 9.0 + (excess * 0.05)
        damage_mult = 11.0 + (excess * 0.08)
    
    return {
        'hp': int(base_hp * hp_mult),
        'speed': int(base_speed * speed_mult),
        'damage': int(base_damage * damage_mult)
    }
Drop Rate de Cartas:
pythondef card_drop_chance(base_rate=0.02, combo=0, perfect_wave=False, mutated=False):
    chance = base_rate
    
    # Bônus de combo
    if combo >= 10:
        chance += 0.01
    if combo >= 50:
        chance += 0.02
    if combo >= 100:
        chance += 0.03
    
    # Bônus Perfect Wave
    if perfect_wave:
        chance += 0.05
    
    # Multiplicador mutado
    if mutated:
        chance *= 3.0
    
    # Cap máximo
    return min(chance, 0.25)  # Max 25%
Cálculo de Score:
pythondef calculate_score(minerals, enemies_killed, bosses_defeated, combo_max, perfect_waves, sector_reached):
    score = 0
    
    # Base
    score += minerals
    score += enemies_killed * 10
    score += bosses_defeated * 500
    
    # Multiplicadores
    score += combo_max * 5
    score += perfect_waves * 100
    score += sector_reached * 50
    
    # Bônus por dificuldade
    if sector_reached >= 50:
        score *= 1.5
    if sector_reached >= 100:
        score *= 2.0
    
    return int(score)
Custo de Fusão de Cartas:
pythondef fusion_cost(current_level, rarity):
    base_cost = {
        'comum': [0, 100, 500, 1500, 3000],
        'incomum': [0, 200, 750, 2000, 4000],
        'epico': [0, 500, 1500, 3500, 6000]
    }
    
    copies_needed = current_level + 1  # Lv1→2 precisa 2, Lv2→3 precisa 3
    minerals = base_cost[rarity][current_level]
    
    required_cards = []
    if current_level >= 3:  # Lv3→4
        required_cards.append('any_uncommon')
    if current_level >= 4:  # Lv4→5
        required_cards.append('any_epic')
    
    return {
        'copies': copies_needed,
        'minerals': minerals,
        'cards': required_cards
    }
Modificadores DDA:
pythondef calculate_dda_modifier(skill_level, performance):
    # Base: 1.0 (sem modificação)
    modifier = 1.0
    
    if skill_level == 'NOOB' and performance == 'struggling':
        modifier = 0.75  # -25% dificuldade
    elif skill_level == 'CASUAL' and performance == 'struggling':
        modifier = 0.85  # -15%
    elif skill_level == 'INTERMEDIARIO' and performance == 'balanced':
        modifier = 1.0   # Normal
    elif skill_level == 'VETERANO' and performance == 'dominating':
        modifier = 1.20  # +20%
    elif skill_level == 'MESTRE' and performance == 'dominating':
        modifier = 1.40  # +40%
    
    return modifier

def apply_dda(enemy_stats, modifier):
    return {
        'hp': int(enemy_stats['hp'] * modifier),
        'speed': int(enemy_stats['speed'] * modifier),
        'damage': int(enemy_stats['damage'] * modifier),
        'spawn_rate': enemy_stats['spawn_rate'] / modifier
    }
```

---

## **APÊNDICE I: Comandos de Debug**

### **Teclas de Debug (Modo Dev):**
```
F1: Invencibilidade toggle
F2: Matar todos inimigos na tela
F3: Debug overlay (FPS, stats, DDA info)
F4: Pular para próximo setor
F5: Spawnar boss atual
F6: +1000 minérios
F7: Dropar carta aleatória
F8: Resetar DDA
F9: Screenshot
F10: Slow motion (50%)
F11: Fast forward (200%)
F12: Desbloquear todas cartas/naves

CTRL+1: Spawnar Kamikaze
CTRL+2: Spawnar Range
CTRL+3: Spawnar Mãe
CTRL+4: Spawnar Mutado aleatório

CTRL+H: Curar completo
CTRL+K: Morrer instantaneamente
CTRL+S: Salvar estado atual
CTRL+L: Carregar estado salvo
```

### **Console de Debug (` ou ~):**
```
> goto_sector 50
> set_hp 999
> set_damage_multiplier 10.0
> spawn kamikaze 10
> unlock_card estabilizador_criogenico
> unlock_ship velocista_raio
> set_skill_level MESTRE
> toggle_dda
> set_spawn_rate 0.1
> clear_enemies
> give_minerals 9999
> unlock_all_achievements
> reset_save
```

---

## **APÊNDICE J: Estrutura de Pastas do Projeto**
```
plane-free/
│
├── assets/
|    ├──
│    │   ├── sprites/
│    │   │   ├── initial/
│    │   │   │   ├── ship_0.png
│    │   │   │   ├── ship_1.png
│    │   │   │   └── ... (ship_7.png)
│    │   │   ├── tanque/
│    │   │   │   ├── fortaleza/ (8 sprites)
│    │   │   │   ├── destruidor/ (8 sprites)
│    │   │   │   └── encouracado/ (8 sprites)
│    │   │   ├── velocista/
│    │   │   └── tecnico/
│    │   │
│    │   ├── enemies/
│    │   │   ├── kamikaze.png
│    │   │   ├── kamikaze_mutated.png
│    │   │   ├── range.png
│    │   │   ├── range_mutated.png
│    │   │   ├── mae.png
│    │   │   ├── mae_mutated.png
│    │   │   └── filhote.png
│    │   │
│    │   ├── bosses/
│    │   │   ├── boss_01/ (3 fases)
│    │   │   ├── boss_02/ (3 fases)
│    │   │   └── ... (boss_14/)
│    │   │
│    │   ├── projectiles/
│    │   │   ├── player_bullet.png
│    │   │   ├── enemy_bullet.png
│    │   │   ├── laser.png
│    │   │   └── missile.png
│    │   │
│    │   ├── particles/
│    │   │   ├── explosion_small/ (frames)
│    │   │   ├── explosion_medium/ (frames)
│    │   │   ├── explosion_large/ (frames)
│    │   │   ├── hit_spark.png
│    │   │   └── trail.png
│    │   │
│    │   ├── cards/
│    │   │   ├── comum/
│    │   │   ├── incomum/
│    │   │   ├── epico/
│    │   │   └── ascensao/
│    │   │
│    │   ├── backgrounds/
│    │   │   ├── troposfera/ (layers)
│    │   │   ├── estratosfera/ (layers)
│    │   │   └── ... (outras atmosferas)
│    │   │
│    │   ├── ui/
│    │   │   ├── hud/
│    │   │   ├── menus/
│    │   │   ├── buttons/
│    │   │   └── icons/
│    │
│    ├── fonts/
│    │   ├── main_font.ttf
│    │   └── monospace.ttf
│    │
│    ├── audio/
│    │   ├── music/
│    │   │   ├── menu_theme.ogg
│    │   │   ├── combat_1.ogg
│    │   │   ├── combat_2.ogg
│    │   │   ├── boss_theme_1.ogg
│    │   │   └── game_over.ogg
│    │   │
│    │   └── sfx/
│    │       ├── player/
│    │       │   ├── shoot.wav
│    │       │   ├── hit.wav
│    │       │   ├── death.wav
│    │       │   └── collect.wav
│    │       ├── enemies/
│    │       ├── bosses/
│    │       └── ui/
│
├── data/
│   ├── cards.json
│   ├── ships.json
│   ├── enemies.json
│   ├── bosses.json
│   ├── achievements.json
│   ├── atmospheres.json
│   └── synergies.json
│
├── src/
│   ├── main.py
│   ├── game.py
│   ├── states/
│   │   ├── menu_state.py
│   │   ├── gameplay_state.py
│   │   ├── pause_state.py
│   │   ├── gameover_state.py
│   │   └── hangar_state.py
│   │
│   ├── entities/
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── boss.py
│   │   ├── projectile.py
│   │   └── collectible.py
│   │
│   ├── systems/
│   │   ├── wave_manager.py
│   │   ├── card_system.py
│   │   ├── ship_registry.py
│   │   ├── achievement_system.py
│   │   ├── dda_manager.py
│   │   ├── spatial_grid.py
│   │   ├── object_pool.py
│   │   └── save_system.py
│   │
│   ├── ui/
│   │   ├── hud.py
│   │   ├── menu.py
│   │   ├── hangar.py
│   │   └── notifications.py
│   │
│   ├── utils/
│   │   ├── input_manager.py
│   │   ├── audio_manager.py
│   │   ├── particle_system.py
│   │   └── helpers.py
│   │
│   └── config.py
│
├── tests/
│   ├── test_collision.py
│   ├── test_cards.py
│   ├── test_dda.py
│   └── test_save_system.py
│
├── docs/
│   ├── GDD_v3.0.md (este documento)
│   ├── API_documentation.md
│   └── changelog.md
│
├── builds/
│   ├── windows/
│   ├── linux/
│   └── mac/
│
├── saves/
│   ├── save.json
│   └── save_backup.json
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```