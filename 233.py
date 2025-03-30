import csv
import random
import os

class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill):
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
        opponent.HP -= self.calculate_damage(opponent)
    
    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            opponent.HP -= self.calculate_damage(opponent, is_magical=True)
        else:
            print("MP不足，无法使用技能！")
            return False
        return True
    
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next:
            self.level_up()
    
    def gain_gold(self, amount):
        self.gold += amount
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.5)
        stats = ["MaxHP", "MaxMP", "ATK", "DEF", "MAT", "MDF", "AGI", "LUK"]
        increments = [20, 10, 3, 2, 3, 2, 1, 1]
        for stat, inc in zip(stats, increments):
            setattr(self, stat, getattr(self, stat) + inc)
        self.HP, self.MP = self.MaxHP, self.MaxMP
        print(f"{self.name} 升级到 {self.level} 级！")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.defense_mode = {player.name: False, enemy.name: False}
    
    def start(self):
        print(f"你遇到了 {self.enemy.name}！")
        self.enemy.HP = self.enemy.MaxHP
        self.enemy.MP = self.enemy.MaxMP
        turn_order = sorted([self.player, self.enemy], key=lambda c: (-c.AGI, c.name == self.player.name))
        
        while self.player.HP > 0 and self.enemy.HP > 0:
            print(f"\n你的生命值: {self.player.HP}/{self.player.MaxHP}, {self.enemy.name}的生命值: {self.enemy.HP}/{self.enemy.MaxHP}")
            for combatant in turn_order:
                if combatant.HP <= 0:
                    continue
                if combatant == self.player:
                    self.player_action()
                else:
                    self.enemy_action()
            self.defense_mode = {self.player.name: False, self.enemy.name: False}
        self.end_battle()
    
    def player_action(self):
        action = input("选择行动 (1. 攻击 2. 使用技能 3. 逃跑 4. 防御): ")
        if action == "1":
            self.player.attack(self.enemy)
        elif action == "2" and not self.player.use_skill(self.enemy):
            return
        elif action == "3":
            print("你成功逃跑了！")
            exit()
        elif action == "4":
            self.defense_mode[self.player.name] = True
        else:
            print("无效的选择，默认攻击！")
            self.player.attack(self.enemy)
    
    def enemy_action(self):
        damage = self.enemy.calculate_damage(self.player)
        if self.defense_mode[self.player.name]:
            damage //= 2
        self.player.HP -= damage
    
    def end_battle(self):
        if self.player.HP > 0:
            print(f"你击败了 {self.enemy.name}！")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gain_gold(self.enemy.gold_reward)
        else:
            print("你被击败了，游戏结束。")
        input("\n按 Enter 继续...")
        clear_screen()

# 数据加载

def load_data(filename, class_type):
    data_list = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_list.append(class_type(**{k: int(v) if v.isdigit() else v for k, v in row.items()}))
    except FileNotFoundError:
        print(f"数据文件 {filename} 未找到！")
        exit()
    return data_list

def choose_class():
    classes = load_data('classes.csv', Character)
    for i, char in enumerate(classes):
        print(f"{i}: {char.name} (MaxHP: {char.MaxHP}, MP: {char.MaxMP}, 技能: {char.skill})")
    return classes[int(input("输入职业编号: "))]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    player = choose_class()
    enemies = load_data('enemies.csv', Enemy)
    while player.HP > 0:
        print(f"当前金币: {player.gold}")
        if input("输入 'q' 退出游戏, Enter 继续战斗: ").lower() == 'q':
            break
        Battle(player, random.choice(enemies)).start()

if __name__ == "__main__":
    main()