import csv
import random
import os

class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skills):
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
        self.skills = skills  # 存储多个技能
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50
        self.gold = 0

    def calculate_damage(self, opponent, is_magical=False):
        if is_magical:
            base_damage = max(1, self.MAT * 4 - opponent.MDF * 2)
        else:
            base_damage = max(1, self.ATK * 4 - opponent.DEF * 2)
        return self.apply_critical_hit(base_damage)

    def apply_critical_hit(self, damage):
        crit_chance = self.LUK / 2  # 暴击率 = LUK / 2%
        if random.randint(1, 100) <= crit_chance:
            crit_multiplier = random.choice([1.5, 2])
            damage = int(damage * crit_multiplier)
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
        return damage
    
    def attack(self, opponent):
        damage = self.calculate_damage(opponent)
        opponent.HP -= damage
        print(f"{self.name} 攻击了 {opponent.name}，造成 {damage} 伤害！")

    def use_skill(self, opponent):
        print("选择技能:")
        for i, skill in enumerate(self.skills):
            print(f"{i + 1}. {skill['name']} (MP: {skill['mp_cost']})")
        choice = input("输入技能编号: ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.skills):
                skill = self.skills[index]
                if self.MP >= skill['mp_cost']:
                    self.MP -= skill['mp_cost']
                    damage = self.calculate_damage(opponent, skill['is_magical']) * skill['multiplier']
                    opponent.HP -= int(damage)
                    print(f"{self.name} 使用 {skill['name']}，造成 {int(damage)} 伤害！(MP -{skill['mp_cost']})")
                else:
                    print("MP不足，无法使用技能！")
            else:
                print("无效的技能选择！")

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
        self.MaxHP += 20
        self.MaxMP += 10
        self.ATK += 3
        self.DEF += 2
        self.MAT += 3
        self.MDF += 2
        self.AGI += 1
        self.LUK += 1
        self.HP = self.MaxHP
        self.MP = self.MaxMP
        print(f"{self.name} 升级到了 {self.level} 级！")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skills, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skills)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

# 读取技能数据
def load_skills():
    skills = {}
    try:
        with open('skills.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                skills[row['name']] = {
                    'name': row['name'],
                    'mp_cost': int(row['mp_cost']),
                    'multiplier': float(row['multiplier']),
                    'is_magical': row['is_magical'].lower() == 'true'
                }
    except FileNotFoundError:
        print("技能数据文件未找到！")
        exit()
    return skills

def load_classes():
    skills = load_skills()
    classes = {}
    try:
        with open('classes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                skill_list = [skills[name] for name in row['skills'].split(';') if name in skills]
                classes[row['id']] = Character(row['name'], int(row['max_hp']), int(row['max_mp']),
                                               int(row['atk']), int(row['defense']), int(row['mat']),
                                               int(row['mdf']), int(row['agi']), int(row['luk']), skill_list)
    except FileNotFoundError:
        print("职业数据文件未找到！")
        exit()
    return classes

def get_battle_order(player, enemy):
    return sorted([player, enemy], key=lambda char: (-char.AGI, char.name == player.name))

def battle(player):
    enemy = Enemy("史莱姆", 50, 10, 5, 2, 3, 2, 5, 2, [], 20, 10)
    turn_order = get_battle_order(player, enemy)
    while player.HP > 0 and enemy.HP > 0:
        for combatant in turn_order:
            if combatant.HP <= 0:
                continue
            if combatant == player:
                action = input("选择行动 (1. 攻击 2. 使用技能): ")
                if action == "1":
                    player.attack(enemy)
                elif action == "2":
                    player.use_skill(enemy)
            else:
                enemy.attack(player)

        if player.HP <= 0:
            print("你被击败了！")
            return
        if enemy.HP <= 0:
            print("你赢了！")
            player.gain_exp(enemy.exp_reward)
            player.gain_gold(enemy.gold_reward)
            return

if __name__ == "__main__":
    classes = load_classes()
    player = classes['1']  # 选择默认职业
    battle(player)
