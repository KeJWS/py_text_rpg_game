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
        damage = self.calculate_damage(opponent)
        opponent.HP -= damage
        print(f"{self.name} 攻击 {opponent.name}，造成 {damage} 伤害！")

    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            damage = self.calculate_damage(opponent, is_magical=True)
            opponent.HP -= damage
            print(f"{self.name} 使用 {self.skill}，造成 {damage} 伤害！ (MP -10)")
        else:
            print("MP不足，无法使用技能！")
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
        print(f"{self.name} 升级到 {self.level} 级！")
        print(f"{self.name}: (MaxHP: {self.MaxHP}, MaxMP: {self.MaxMP}, ATK: {self.ATK}, DEF: {self.DEF}, MAT: {self.MAT}, MDF: {self.MDF}, AGI: {self.AGI}, LUK: {self.LUK}, 技能: {self.skill})")

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
        self.turn_order = self.get_battle_order()
    
    def get_battle_order(self):
        """根据敏捷（AGI）排序，敏捷高的角色先行动。若敏捷相同，玩家优先"""
        return sorted([self.player, self.enemy], key=lambda char: (-char.AGI, char.name == self.player.name))
    
    def player_action(self):
        action = input("选择行动 (a. 攻击 s. 使用技能 q. 逃跑 d. 防御): ")
        if action == "a":
            self.player.attack(self.enemy)
        elif action == "s":
            if not self.player.use_skill(self.enemy):
                return False  # 取消行动
        elif action == "q":
            if self.try_escape():
                return True  # 逃跑成功，战斗结束
        elif action == "d":
            self.defense_mode[self.player.name] = True
            print("你进入防御状态，本回合受到的伤害减少50%！")
        else:
            print("无效的选择，默认攻击！")
            self.player.attack(self.enemy)
        return False
    
    def enemy_action(self):
        damage = self.enemy.calculate_damage(self.player)
        if self.defense_mode[self.player.name]:
            damage //= 2  # 玩家防御时伤害减少50%
        self.player.HP -= damage
        print(f"{self.enemy.name} 攻击了你，造成 {damage} 伤害！")
    
    def try_escape(self):
        escape_chance = min(90, max(10, self.player.AGI * 3))  # 逃跑概率：10% - 90%
        if random.randint(1, 100) <= escape_chance:
            print("你成功逃跑了！")
            return True
        else:
            print("逃跑失败！")
            return False
    
    def process_battle(self):
        print(f"你遇到了 {self.enemy.name}！")
        while self.player.HP > 0 and self.enemy.HP > 0:
            print(f"\n你的生命值: {self.player.HP}/{self.player.MaxHP}, {self.enemy.name}的生命值: {self.enemy.HP}/{self.enemy.MaxHP}")
            for combatant in self.turn_order:
                if combatant.HP <= 0:
                    continue
                
                if combatant == self.player:
                    if self.player_action():
                        return  # 逃跑成功，结束战斗
                else:
                    self.enemy_action()
            
            # 清除防御状态
            self.defense_mode = {self.player.name: False, self.enemy.name: False}
        
        self.battle_result()
    
    def battle_result(self):
        if self.player.HP > 0:
            print(f"你击败了 {self.enemy.name}！")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gain_gold(self.enemy.gold_reward)
        else:
            print("你被击败了，游戏结束。")

        input("\n按 Enter 继续...")
        clear_screen()

def battle(player):
    enemy = get_random_enemy()
    battle_instance = Battle(player, enemy)
    battle_instance.process_battle()

def load_classes():
    classes = {}
    try:
        with open('classes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                classes[row['id']] = Character(
                    row['name'],
                    int(row['max_hp']),int(row['max_mp']),int(row['atk']),int(row['defense']),
                    int(row['mat']),int(row['mdf']),int(row['agi']),int(row['luk']),
                    row['skill']
                )
    except FileNotFoundError:
        print("职业数据文件未找到！")
        exit()
    except Exception as e:
        print(f"读取职业数据时出错: {e}")
        exit()
    return classes

def load_enemies():
    enemies = []
    try:
        with open('enemies.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                enemies.append(Enemy(
                    row['name'],
                    int(row['max_hp']),int(row['max_mp']),int(row['atk']),int(row['defense']),
                    int(row['mat']),int(row['mdf']),int(row['agi']),int(row['luk']),
                    row['skill'],
                    int(row['exp_reward']),
                    int(row['gold_reward'])
                ))
    except FileNotFoundError:
        print("敌人数据文件未找到！")
        exit()
    except Exception as e:
        print(f"读取敌人数据时出错: {e}")
        exit()
    return enemies

# 在游戏开始时加载敌人
enemies = load_enemies()

def get_random_enemy():
    return random.choice(enemies)

def choose_class():
    classes = load_classes()
    print("选择你的职业:")
    for key, char in classes.items():
        print(f"{key}: {char.name} (MaxHP: {char.MaxHP}, MaxMP: {char.MaxMP}, ATK: {char.ATK}, DEF: {char.DEF}, MAT: {char.MAT}, MDF: {char.MDF}, AGI: {char.AGI}, LUK: {char.LUK}, 技能: {char.skill})")
    
    choice = input("请输入对应的数字: ")
    if choice in classes:
        return classes[choice]
    else:
        print("无效的职业选择，默认选择战士。")
        return classes.get("1")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("欢迎来到文字RPG冒险！")
    player = choose_class()
    print(f"你选择了 {player.name}，冒险开始！")
    
    while player.HP > 0:
        print(f"\n当前金币: {player.gold}")
        print(f"HP: {player.HP}/{player.MaxHP}")
        print(f"MP: {player.MP}/{player.MaxMP}")
        print(f"EXP: {player.exp}/{player.exp_to_next}")
        print(f"暴击率: {player.LUK/2}%")
        command = input("输入 'q' 退出游戏, 按 Enter 继续战斗: ")
        if command.lower() == 'q':
            print("游戏结束，再见！")
            break
        battle(player)
        if player.HP > 0:
            player.HP = min(player.MaxHP, player.HP + int(player.MaxHP*0.2))  # 战斗后恢复部分HP
            player.MP = min(player.MaxMP, player.MP + int(player.MaxMP*0.1))  # 战斗后恢复部分MP
            print("你恢复了一部分生命值和魔法值，准备迎接下一个挑战！")

if __name__ == "__main__":
    main()