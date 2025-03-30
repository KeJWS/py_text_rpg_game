import random

class Weapon:
    def __init__(self, name, attack_bonus):
        self.name = name
        self.attack_bonus = attack_bonus

    def __str__(self):
        return f"{self.name} (ATK + {self.attack_bonus})"

class Equipment:
    def __init__(self, name, defense_bonus, health_bonus):
        self.name = name
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus

    def __str__(self):
        return f"{self.name} (DEF + {self.defense_bonus}, MaxHP + {self.health_bonus})"

class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, weapon=None, equipment=None):
        self.name = name
        self.MaxHP = max_hp
        self.MaxMP = max_mp
        self.HP = max_hp
        self.MP = max_mp
        self.ATK = atk
        self.DEF = defense
        self.MAT = mat
        self.MDF = mdf
        self.AGI = agi
        self.LUK = luk
        self.skill = skill
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50
        self.gold = 0
        self.weapon = weapon
        self.equipment = equipment
        self.inventory = Inventory()

    def equip_weapon(self, weapon):
        """装备或脱下武器"""
        if weapon is None:
            if self.weapon:
                print(f"{self.name} 脱下了 {self.weapon.name}。ATK-{self.weapon.attack_bonus}")
                self.ATK -= self.weapon.attack_bonus
            self.weapon = None
            print(f"{self.name} 现在没有武器。")
        else:
            if self.weapon:
                self.ATK -= self.weapon.attack_bonus
            self.weapon = weapon
            self.ATK += weapon.attack_bonus
            print(f"{self.name} 装备了 {weapon.name}，ATK+{weapon.attack_bonus}。")

    def equip_armor(self, equipment):
        """装备或脱下防具"""
        if equipment is None:
            if self.equipment:
                print(f"{self.name} 脱下了 {self.equipment.name}。DEF-{self.equipment.defense_bonus}, MaxHP-{self.equipment.health_bonus}")
                self.DEF -= self.equipment.defense_bonus
                self.MaxHP -= self.equipment.health_bonus
            self.equipment = None
            print(f"{self.name} 现在没有防具。")
        else:
            if self.equipment:
                self.DEF -= self.equipment.defense_bonus
                self.MaxHP -= self.equipment.health_bonus
            self.equipment = equipment
            self.DEF += equipment.defense_bonus
            self.MaxHP += equipment.health_bonus
            print(f"{self.name} 装备了 {equipment.name}，DEF+{equipment.defense_bonus}, MaxHP+{equipment.health_bonus}")

    def calculate_damage(self, opponent, is_magical=False):
        stat_attack = self.MAT if is_magical else self.ATK
        stat_defense = opponent.MDF if is_magical else opponent.DEF
        base_damage = max(1, stat_attack * 4 - stat_defense * 2)
        return self.apply_critical_hit(base_damage)
    
    def apply_critical_hit(self, damage):
        if random.randint(1, 100) <= self.LUK / 2:
            crit_multiplier = random.choice([1.5, 2])
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
            return int(damage * crit_multiplier)
        return damage

    def attack(self, opponent):
        damage = self.calculate_damage(opponent)
        opponent.HP -= damage
        print(f"🗡️ {self.name} 攻击 {opponent.name}，造成 \033[33m{damage}\033[0m 伤害！")

    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            damage = self.calculate_damage(opponent, is_magical=True)
            opponent.HP -= damage
            print(f"✨ {self.name} 释放了技能 {self.skill}，造成 {damage} 伤害！ (MP -10)")
        else:
            print("❌ 技能释放失败，MP不足！")
            return False
        return True

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
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.5)
        stats = ["MaxHP", "MaxMP", "ATK", "DEF", "MAT", "MDF", "AGI", "LUK"]
        increments = [20, 10, 3, 2, 3, 2, 1, 1]
        for stat, inc in zip(stats, increments):
            setattr(self, stat, getattr(self, stat) + inc)
        self.HP, self.MP = self.MaxHP, self.MaxMP
        print(f"\033[33m{self.name} 升级到 {self.level} 级！\033[0m")
        print(f"{self.name}: (MaxHP: {self.MaxHP}, MaxMP: {self.MaxMP}, ATK: {self.ATK}, DEF: {self.DEF}, MAT: {self.MAT}, MDF: {self.MDF}, AGI: {self.AGI}, LUK: {self.LUK}, 技能: {self.skill})")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward, min_level=1, max_level=99):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.weapon = None
        self.equipment = None
        self.min_level = min_level
        self.max_level = max_level

    def equip_weapon(self, weapon):
        """敌人装备武器"""
        self.weapon = weapon
        self.ATK += weapon.attack_bonus

    def equip_armor(self, equipment):
        """敌人装备防具"""
        self.equipment = equipment
        self.DEF += equipment.defense_bonus
        self.MaxHP += equipment.health_bonus

class Item:
    def __init__(self, item_id, name, item_type, effect, value, price):
        self.id = int(item_id)
        self.name = name
        self.type = item_type  # 恢复 / 战斗 / 任务
        self.effect = effect  # HP / MP / ATK / DEF
        self.value = int(value)  # 数值
        self.price = int(price)  # 价格

    def use(self, target):
        """使用物品，作用于目标角色"""
        if self.type == "恢复":
            if self.effect == "HP":
                target.HP = min(target.MaxHP, target.HP + self.value)
                print(f"✨ {target.name} 使用了 {self.name}，恢复 {self.value} 生命值！")
            elif self.effect == "MP":
                target.MP = min(target.MaxMP, target.MP + self.value)
                print(f"🔮 {target.name} 使用了 {self.name}，恢复 {self.value} 魔法值！")
        elif self.type == "战斗":
            setattr(target, self.effect, getattr(target, self.effect) + self.value)
            print(f"🔥 {target.name} 使用了 {self.name}，{self.effect} 提高了 {self.value}！")

class Inventory:
    def __init__(self):
        self.items = {}  # 存储物品 {item_id: 数量}

    def add_item(self, item, quantity=1):
        """添加物品到背包"""
        if item.id in self.items:
            self.items[item.id] += quantity
        else:
            self.items[item.id] = quantity
        print(f"🎒 获得物品: {item.name} x{quantity}")

    def remove_item(self, item, quantity=1):
        """移除物品"""
        if item.id in self.items:
            if self.items[item.id] > quantity:
                self.items[item.id] -= quantity
            else:
                del self.items[item.id]
            print(f"🗑️ 使用了 {item.name} x{quantity}")
        else:
            print("⚠️ 没有这个物品！")

    def view_inventory(self, item_list):
        """查看背包"""
        print("\n🎒 你的背包:")
        if not self.items:
            print("（空）")
        for item_id, quantity in self.items.items():
            item = item_list[item_id]
            print(f"{item.name} x{quantity} ({item.type})")

    def use_item(self, item_id, target, item_list):
        """使用背包中的物品"""
        if item_id in self.items:
            item = item_list[item_id]
            item.use(target)
            self.remove_item(item)
        else:
            print("⚠️ 你没有这个物品！")

class Shop:
    def __init__(self, items):
        """初始化商店，选择可出售的物品"""
        self.items_for_sale = {id_: item for id_, item in items.items()}

    def display_items(self):
        """显示商店可购买的商品"""
        print("\n🛒 商店：")
        print("ID   |   物品名      效果        效果值      价格")
        print("-" * 60)
        for item in self.items_for_sale.values():
            print(f"{item.id:2} |   {item.name:6}      {item.effect:3}     +{item.value:3}      {item.price:3} G")
        print("-" * 60)

    def buy_item(self, player, item_id):
        """购买物品"""
        if item_id in self.items_for_sale:
            item = self.items_for_sale[item_id]
            if player.gold >= item.price:
                player.gold -= item.price
                player.inventory.add_item(item)
                print(f"✅ 你成功购买了 {item.name}！")
            else:
                print("⚠️ 你的金币不足！")
        else:
            print("⚠️ 物品不存在！")

