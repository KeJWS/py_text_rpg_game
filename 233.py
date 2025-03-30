import random

class Equipment:
    """基类，代表武器或防具"""
    def __init__(self, name, atk_bonus=0, def_bonus=0, hp_bonus=0):
        self.name = name
        self.atk_bonus = atk_bonus
        self.def_bonus = def_bonus
        self.hp_bonus = hp_bonus
    
    def __str__(self):
        return f"{self.name} (ATK+{self.atk_bonus}, DEF+{self.def_bonus}, MaxHP+{self.hp_bonus})"

class Character:
    """游戏角色基类"""
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill):
        self.name = name
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.hp = max_hp
        self.mp = max_mp
        self.atk = atk
        self.defense = defense
        self.mat = mat
        self.mdf = mdf
        self.agi = agi
        self.luk = luk
        self.skill = skill
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50
        self.gold = 0
        self.weapon = None
        self.armor = None
        self.inventory = Inventory()
    
    def equip(self, item):
        """装备武器或防具"""
        if isinstance(item, Equipment):
            if item.atk_bonus:  # 说明是武器
                self._change_weapon(item)
            else:  # 说明是防具
                self._change_armor(item)
    
    def _change_weapon(self, weapon):
        if self.weapon:
            self.atk -= self.weapon.atk_bonus
        self.weapon = weapon
        self.atk += weapon.atk_bonus

    def _change_armor(self, armor):
        if self.armor:
            self.defense -= self.armor.def_bonus
            self.max_hp -= self.armor.hp_bonus
        self.armor = armor
        self.defense += armor.def_bonus
        self.max_hp += armor.hp_bonus

    def attack(self, opponent):
        damage = self._calculate_damage(opponent)
        opponent.hp -= damage
        print(f"{self.name} 攻击 {opponent.name}，造成 {damage} 伤害！")
    
    def _calculate_damage(self, opponent, is_magical=False):
        attack_stat = self.mat if is_magical else self.atk
        defense_stat = opponent.mdf if is_magical else opponent.defense
        base_damage = max(1, attack_stat * 4 - defense_stat * 2)
        return self._apply_critical(base_damage)

    def _apply_critical(self, damage):
        if random.randint(1, 100) <= self.luk / 2:
            crit_multiplier = random.choice([1.5, 2])
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
            return int(damage * crit_multiplier)
        return damage
    
    def use_skill(self, opponent):
        if self.mp >= 10:
            self.mp -= 10
            damage = self._calculate_damage(opponent, is_magical=True)
            opponent.hp -= damage
            print(f"{self.name} 释放 {self.skill}，造成 {damage} 伤害！（MP-10）")
        else:
            print("技能释放失败，MP不足！")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} 获得 {amount} 经验值！")
        if self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.5)
        self.max_hp += 20
        self.max_mp += 10
        self.atk += 3
        self.defense += 2
        self.mat += 3
        self.mdf += 2
        self.agi += 1
        self.luk += 1
        self.hp, self.mp = self.max_hp, self.max_mp
        print(f"{self.name} 升级到 {self.level} 级！")

class Enemy(Character):
    """敌人类，继承自 Character"""
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

class Item:
    """物品类"""
    def __init__(self, item_id, name, item_type, effect, value, price):
        self.id = int(item_id)
        self.name = name
        self.type = item_type
        self.effect = effect
        self.value = int(value)
        self.price = int(price)

    def use(self, target):
        if self.type == "恢复":
            if self.effect == "HP":
                target.hp = min(target.max_hp, target.hp + self.value)
                print(f"{target.name} 使用 {self.name}，恢复 {self.value} 生命值！")
            elif self.effect == "MP":
                target.mp = min(target.max_mp, target.mp + self.value)
                print(f"{target.name} 使用 {self.name}，恢复 {self.value} 魔法值！")
        elif self.type == "战斗":
            setattr(target, self.effect, getattr(target, self.effect) + self.value)
            print(f"{target.name} 使用 {self.name}，{self.effect} 提高 {self.value}！")

class Inventory:
    """背包系统"""
    def __init__(self):
        self.items = {}
    
    def add_item(self, item, quantity=1):
        self.items[item.id] = self.items.get(item.id, 0) + quantity
        print(f"获得 {item.name} x{quantity}")
    
    def remove_item(self, item, quantity=1):
        if item.id in self.items and self.items[item.id] >= quantity:
            self.items[item.id] -= quantity
            if self.items[item.id] == 0:
                del self.items[item.id]
            print(f"使用 {item.name} x{quantity}")
        else:
            print("没有足够的该物品！")
    
    def use_item(self, item_id, target, item_list):
        if item_id in self.items:
            item = item_list[item_id]
            item.use(target)
            self.remove_item(item)
        else:
            print("你没有这个物品！")
