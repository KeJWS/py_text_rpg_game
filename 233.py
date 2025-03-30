class Enemy:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward, min_level=1, max_level=99):
        self.name = name
        self.MaxHP = max_hp
        self.HP = max_hp
        self.MaxMP = max_mp
        self.MP = max_mp
        self.ATK = atk
        self.DEF = defense
        self.MAT = mat
        self.MDF = mdf
        self.AGI = agi
        self.LUK = luk
        self.skill = skill
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.min_level = min_level
        self.max_level = max_level

    def calculate_damage(self, opponent, is_magical=False):
        """计算敌人攻击玩家的伤害"""
        stat_attack = self.MAT if is_magical else self.ATK
        stat_defense = opponent.MDF if is_magical else opponent.DEF
        base_damage = max(1, stat_attack * 4 - stat_defense * 2)  # 计算伤害，确保不低于1
        return self.apply_critical_hit(base_damage)

    def apply_critical_hit(self, damage):
        """计算暴击伤害"""
        if random.randint(1, 100) <= self.LUK / 2:  # 根据敌人的运气（LUK）决定暴击
            crit_multiplier = random.choice([1.5, 2])
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
            return int(damage * crit_multiplier)
        return damage

    def equip_weapon(self, weapon):
        """敌人装备武器"""
        self.weapon = weapon
        self.ATK += weapon.attack_bonus

    def equip_armor(self, equipment):
        """敌人装备防具"""
        self.equipment.append(equipment)
        self.DEF += equipment.defense_bonus
        self.MaxHP += equipment.health_bonus
