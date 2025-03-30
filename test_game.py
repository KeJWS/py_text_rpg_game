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
        if is_magical:
            damage = max(1, self.MAT * 4 - opponent.MDF * 2)
        else:
            damage = max(1, self.ATK * 4 - opponent.DEF * 2)
        return damage
    
    def attack(self, opponent):
        damage = self.calculate_damage(opponent)
        opponent.HP -= damage
        print(f"{self.name} 攻击了 {opponent.name}，造成 {damage} 伤害！")
    
    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            damage = self.calculate_damage(opponent, is_magical=True)
            opponent.HP -= damage
            print(f"{self.name} 使用了 {self.skill}，造成 {damage} 伤害！ (MP -10)")
        else:
            print("MP不足，无法使用技能！")
            return False
        return True
    
    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} 获得了 {amount} 经验值！")
        if self.exp >= self.exp_to_next:
            self.level_up()
    
    def gain_gold(self, amount):
        self.gold += amount
        print(f"{self.name} 获得了 {amount} 金币！ (当前金币: {self.gold})")

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
        self.AGI += 1  # 升级增加敏捷
        self.LUK += 1
        self.HP = self.MaxHP
        self.MP = self.MaxMP
        print(f"{self.name} 升级到了等级 {self.level}！所有属性提升，生命值和魔法值已恢复！")
        print(f"{self.name}: (MaxHP: {self.MaxHP}, MaxMP: {self.MaxMP}, ATK: {self.ATK}, DEF: {self.DEF}, MAT: {self.MAT}, MDF: {self.MDF}, AGI: {self.AGI}, LUK: {self.LUK}, 技能: {self.skill})")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward  # 敌人掉落金币

def load_classes():
    classes = {}
    try:
        with open('classes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                classes[row['id']] = Character(
                    row['name'],
                    int(row['max_hp']),
                    int(row['max_mp']),
                    int(row['atk']),
                    int(row['defense']),
                    int(row['mat']),
                    int(row['mdf']),
                    int(row['agi']),
                    int(row['luk']),
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
                    int(row['max_hp']),
                    int(row['max_mp']),
                    int(row['atk']),
                    int(row['defense']),
                    int(row['mat']),
                    int(row['mdf']),
                    int(row['agi']),
                    int(row['luk']),
                    row['skill'],
                    int(row['exp_reward']),
                    int(row['gold_reward'])  # 读取金币奖励
                ))
    except FileNotFoundError:
        print("敌人数据文件未找到！")
        exit()
    except Exception as e:
        print(f"读取敌人数据时出错: {e}")
        exit()
    return enemies

def choose_class():
    classes = load_classes()  # 从 CSV 加载职业
    print("选择你的职业:")
    for key, char in classes.items():
        print(f"{key}: {char.name} (MaxHP: {char.MaxHP}, MaxMP: {char.MaxMP}, ATK: {char.ATK}, DEF: {char.DEF}, MAT: {char.MAT}, MDF: {char.MDF}, AGI: {char.AGI}, LUK: {char.LUK}, 技能: {char.skill})")
    
    choice = input("请输入对应的数字: ")
    if choice in classes:
        return classes[choice]
    else:
        print("无效的职业选择，默认选择战士。")
        return classes.get("1")  # 或者提供更合理的默认选项

# 在游戏开始时加载敌人
enemies = load_enemies()

def get_random_enemy():
    return random.choice(enemies)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows 使用 cls, 其他系统使用 clear

def get_battle_order(player, enemy):
    """根据敏捷（AGI）排序，敏捷高的角色先行动。若敏捷相同，玩家优先"""
    return sorted([player, enemy], key=lambda char: (-char.AGI, char.name == player.name))

def battle(player):
    enemy = get_random_enemy()
    enemy.HP = enemy.MaxHP  # 确保敌人是满血状态
    enemy.MP = enemy.MaxMP
    print(f"你遇到了 {enemy.name}！")
    
    defense_mode = {player.name: False, enemy.name: False}  # 记录防御状态
    turn_order = get_battle_order(player, enemy)  # 排序行动顺序

    while player.HP > 0 and enemy.HP > 0:
        print(f"\n你的生命值: {player.HP}/{player.MaxHP}, {enemy.name}的生命值: {enemy.HP}/{enemy.MaxHP}")

        for combatant in turn_order:
            if combatant.HP <= 0:
                continue  # 角色已死亡，跳过回合

            if combatant == player:  # 玩家行动
                action = input("选择行动 (1. 攻击 2. 使用技能 3. 逃跑 4. 防御): ")

                if action == "1":
                    player.attack(enemy)
                elif action == "2":
                    if not player.use_skill(enemy):
                        continue
                elif action == "3":
                    print("你成功逃跑了！")
                    return
                elif action == "4":
                    defense_mode[player.name] = True
                    print("你进入防御状态，本回合受到的伤害减少50%！")
                else:
                    print("无效的选择，默认攻击！")
                    player.attack(enemy)
                    continue
            
            else:  # 敌人行动
                damage = enemy.calculate_damage(player)
                if defense_mode[player.name]:
                    damage //= 2  # 玩家防御时伤害减少50%
                player.HP -= damage
                print(f"{enemy.name} 攻击了你，造成 {damage} 伤害！")

        # 清除防御状态
        defense_mode = {player.name: False, enemy.name: False}

    if player.HP > 0:
        print(f"你击败了 {enemy.name}！")
        player.gain_exp(enemy.exp_reward)
        player.gain_gold(enemy.gold_reward)  # 战斗胜利获得金币
    else:
        print("你被击败了，游戏结束。")

    input("\n按 Enter 继续...")  # 暂停，避免信息消失
    clear_screen()  # 清屏

def main():
    print("欢迎来到文字RPG冒险！")
    player = choose_class()
    print(f"你选择了 {player.name}，冒险开始！")
    
    while player.HP > 0:
        print(f"\n当前金币: {player.gold}")
        print(f"HP: {player.HP}/{player.MaxHP}")
        print(f"MP: {player.MP}/{player.MaxMP}")
        print(f"EXP: {player.exp}/{player.exp_to_next}")
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
