import game_data

import random

class Weapon:
    def __init__(self, id, name, attack_bonus, price, note):
        self.id = id
        self.name = name
        self.attack_bonus = attack_bonus
        self.price = price
        self.note = note

    def __str__(self):
        return f"{self.name} (ATK + {self.attack_bonus})"

class Equipment:
    def __init__(self, id, name, defense_bonus, health_bonus, price, note):
        self.id = id
        self.name = name
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus
        self.price = price
        self.note = note

    def __str__(self):
        return f"{self.name} (DEF + {self.defense_bonus}, MaxHP + {self.health_bonus})"

class Shield(Equipment):
    def __init__(self, id, name, defense_bonus, price, note):
        super().__init__(id, name, defense_bonus, price, note)
        self.id = id
        self.name = name
        self.defense_bonus = defense_bonus
        self.price = price
        self.note = note

    def __str__(self):
        return f"{self.name} (DEF + {self.defense_bonus})"

class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill):
        self.base_stats = {
            "MaxHP": max_hp, "MaxMP": max_mp, "ATK": atk, "DEF": defense,
            "MAT": mat, "MDF": mdf, "AGI": agi, "LUK": luk
        }
        self.name = name
        self.MaxHP, self.MaxMP, self.ATK, self.DEF = max_hp, max_mp, atk, defense
        self.MAT, self.MDF, self.AGI, self.LUK = mat, mdf, agi, luk
        self.HP, self.MP = max_hp, max_mp
        self.skill = skill
        self.level, self.exp, self.exp_to_next, self.gold = 1, 0, 50, 0
        self.weapon, self.equipment = None, None
        self.weapons, self.armors = {}, {}
        self.inventory = Inventory()

    def add_weapon(self, weapon):
        self.weapons[weapon.id] = weapon
        print(f"🔪 {self.name} 获得了武器 {weapon.name}！")

    def add_armor(self, armor):
        self.armors[armor.id] = armor
        print(f"🛡️ {self.name} 获得了防具 {armor.name}！")

    def unequip_weapon(self):
        if self.weapon:
            print(f"{self.name} 脱下了 {self.weapon.name}。ATK-{self.weapon.attack_bonus}")
            self.ATK -= self.weapon.attack_bonus
            self.weapon = None

    def equip_weapon(self, weapon_id):
        if weapon_id in self.weapons:
            self.unequip_weapon()
            self.weapon = self.weapons[weapon_id]
            self.ATK += self.weapon.attack_bonus
            print(f"{self.name} 装备了 {self.weapon.name}，ATK+{self.weapon.attack_bonus}。")
        else:
            print("⚠️ 你没有这把武器！")

    def unequip_armor(self):
        if self.equipment:
            print(f"{self.name} 脱下了 {self.equipment.name}。DEF-{self.equipment.defense_bonus}, MaxHP-{self.equipment.health_bonus}")
            self.DEF -= self.equipment.defense_bonus
            self.MaxHP -= self.equipment.health_bonus
            self.equipment = None

    def equip_armor(self, armor_id):
        if armor_id in self.armors:
            self.unequip_armor()
            self.equipment = self.armors[armor_id]
            self.DEF += self.equipment.defense_bonus
            self.MaxHP += self.equipment.health_bonus
            print(f"{self.name} 装备了 {self.equipment.name}，DEF+{self.equipment.defense_bonus}, MaxHP+{self.equipment.health_bonus}")
        else:
            print("⚠️ 你没有这件防具！")

    def attack(self, opponent):
        damage = self.calculate_damage(opponent)
        opponent.HP = max(0, opponent.HP - damage)
        print(f"🗡️ {self.name} 攻击 {opponent.name}，造成 {damage} 伤害！")

    def calculate_damage(self, opponent, is_magical=False):
        stat_attack = self.MAT if is_magical else self.ATK
        stat_defense = opponent.MDF if is_magical else opponent.DEF
        base_damage = max(1, stat_attack * 4 - stat_defense * 2)
        return self.apply_critical_hit(base_damage)

    def apply_critical_hit(self, damage):
        if random.randint(1, 100) <= self.LUK / 2:
            crit_multiplier = random.choice([1.5, 2])
            print(f"💥 {self.name} 造成暴击！伤害 x{crit_multiplier}")
            return int(damage * crit_multiplier)
        return damage

    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            damage = self.calculate_damage(opponent, is_magical=True)
            opponent.HP = max(0, opponent.HP - damage)
            print(f"✨ {self.name} 释放 {self.skill}，造成 {damage} 伤害！ (MP -10)")
        else:
            print("❌ 技能释放失败，MP不足！")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} 获得 {amount} 经验值！")
        if self.exp >= self.exp_to_next:
            self.level_up()

    def gain_gold(self, amount):
        self.gold += amount
        print(f"{self.name} 获得 {amount} 金币！(当前金币: {self.gold})")

    def level_up(self):
        self.level += 1
        self.exp, self.exp_to_next = 0, int(self.exp_to_next * 1.5)
        growth = {"MaxHP": 20, "MaxMP": 10, "ATK": 3, "DEF": 2, "MAT": 3, "MDF": 2, "AGI": 1, "LUK": 1}
        for stat, inc in growth.items():
            setattr(self, stat, getattr(self, stat) + inc)
        self.HP, self.MP = self.MaxHP, self.MaxMP
        print(f"🎉 {self.name} 升级到 {self.level} 级！")

    def reset_stats(self):
        print("✨ 你的属性被重置！但装备和金币得到了保留！")
        self.level, self.exp, self.exp_to_next = 1, 0, 50
        for stat, value in self.base_stats.items():
            setattr(self, stat, value)
        self.HP, self.MP = self.MaxHP, self.MaxMP

class Enemy(Character):
    def __init__(self, id, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward, min_level=1, max_level=99):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.id = id
        self.exp_reward, self.gold_reward = exp_reward, gold_reward
        self.min_level, self.max_level = min_level, max_level
