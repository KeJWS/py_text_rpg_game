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
        self.level, self.exp, self.exp_to_next, self.gold = 1, 0, 1, 999
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
        opponent.HP -= damage
        print(f"🗡️ {self.name} 攻击 {opponent.name}，造成 \033[33m{damage}\033[0m 伤害！")

    def calculate_damage(self, opponent, is_magical=False):
        stat_attack = self.MAT if is_magical else self.ATK
        stat_defense = opponent.MDF if is_magical else opponent.DEF
        base_damage = max(1, stat_attack * 4 - stat_defense * 2)
        return self.apply_critical_hit(base_damage)

    def apply_critical_hit(self, damage):
        if random.randint(1, 100) <= self.LUK / 2:
            crit_multiplier = random.choice([1.5, 2, 2.5])
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
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
        print(f"{self.name} 获得 {amount} 金币！(当前\033[33m金币: {self.gold}\033[0m)")

    def level_up(self):
        self.level += 1
        self.exp, self.exp_to_next = 0, int(1 * (self.level ** 1.5))
        growth = {"MaxHP": 20, "MaxMP": 10, "ATK": 3, "DEF": 2, "MAT": 3, "MDF": 2, "AGI": 1, "LUK": 1}
        for stat, inc in growth.items():
            setattr(self, stat, getattr(self, stat) + inc)
        self.HP, self.MP = self.MaxHP, self.MaxMP
        print(f"🎉 \033[33m{self.name} 升级到 {self.level} 级！\033[0m")

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

class Item:
    def __init__(self, item_id, name, item_type, effect, value, price, note):
        self.id = int(item_id)
        self.name = name
        self.type = item_type
        self.effect = effect
        self.value = int(value)
        self.price = int(price)
        self.note = int(note)

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
            print(f"{item.id}, {item.name} x{quantity}")

    def use_item(self, item_id, target, item_list):
        """使用背包中的物品"""
        if item_id in self.items:
            item = item_list[item_id]
            item.use(target)
            self.remove_item(item)
        else:
            print("⚠️ 你没有这个物品！")

class ItemShop:
    def __init__(self, items):
        """初始化物品商店"""
        self.items_for_sale = {k: v for k, v in items.items() if v.note != 1}  # 过滤掉 note=1 的物品

    def display_items(self):
        """显示商店中的物品"""
        print("\n🛒 物品商店：")
        print("ID   |   名称        类型       效果        价格")
        print("-" * 50)
        for item in self.items_for_sale.values():
            print(f"{item.id:2} | {item.name:6}  {item.type:3}      {item.effect:3} +{item.value:3}    {item.price:3} G")
        print("-" * 50)

    def buy_item(self, player, item_id):
        """购买物品"""
        if item_id in self.items_for_sale:
            item = self.items_for_sale[item_id]
            if player.gold >= item.price:
                player.gold -= item.price
                player.inventory.add_item(item)
                print(f"✅ 你成功购买了 {item.name}！(剩余金币: {player.gold})")
            else:
                print("⚠️ 你的金币不足！")
        else:
            print("⚠️ 物品不存在！")


class WeaponShop:
    def __init__(self, weapons):
        """初始化武器商店"""
        self.weapons_for_sale = {k: v for k, v in weapons.items() if v.note != 1}

    def display_items(self):
        """显示商店中的武器"""
        print("\n🔪 武器商店：")
        print("ID   |   名称    攻击力加成  价格")
        print("-" * 70)
        for weapon in self.weapons_for_sale.values():
            print(f"{weapon.id:3}   |   {weapon.name:6}     ATK+{weapon.attack_bonus:2}     {weapon.price:3} G")
        print("-" * 70)

    def buy_item(self, player, weapon_id):
        """购买武器"""
        if weapon_id in self.weapons_for_sale:
            weapon = self.weapons_for_sale[weapon_id]
            if player.gold >= weapon.price:
                player.gold -= weapon.price
                player.add_weapon(weapon)
                print(f"✅ 你成功购买了 {weapon.name}！(剩余金币: {player.gold})")
            else:
                print("⚠️ 你的金币不足！")
        else:
            print("⚠️ 武器不存在！")

class ArmorShop:
    def __init__(self, armors):
        """初始化护甲商店"""
        self.armors_for_sale = {k: v for k, v in armors.items() if v.note != 1}

    def display_items(self):
        """显示商店中的护甲"""
        print("\n🛡️ 护甲商店：")
        print("ID   |   名称    防御力加成  生命加成    价格")
        print("-" * 70)
        for armor in self.armors_for_sale.values():
            print(f"{armor.id:3}    |   {armor.name:6}  DEF+{armor.defense_bonus:2}     HP+{armor.health_bonus:2}   {armor.price:3} G")
        print("-" * 70)

    def buy_item(self, player, armor_id):
        """购买护甲"""
        if armor_id in self.armors_for_sale:
            armor = self.armors_for_sale[armor_id]
            if player.gold >= armor.price:
                player.gold -= armor.price
                player.add_armor(armor)
                print(f"✅ 你成功购买了 {armor.name}！(剩余金币: {player.gold})")
            else:
                print("⚠️ 你的金币不足！")
        else:
            print("⚠️ 护甲不存在！")

class Map:
    def __init__(self, name, enemy_ids):
        self.name = name  # 地图名称
        self.enemy_ids = enemy_ids  # 可刷怪物的ID列表

    def get_enemy(self, player_level):
        """根据玩家等级返回该地图的怪物"""
        enemies = game_data.load_enemies()
        available_enemies = [e for e in enemies if e.id in self.enemy_ids and e.min_level <= player_level <= e.max_level]
        return random.choice(available_enemies) if available_enemies else None  # 若没有符合条件的怪物则返回 None
