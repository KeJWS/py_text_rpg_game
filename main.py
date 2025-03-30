import csv
import random
import os
from game_data import load_classes, load_enemies, load_weapons, load_armor
from character import Character, Enemy, Weapon, Equipment

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

# 在游戏开始时加载敌人
enemies = load_enemies()

def get_random_enemy():
    enemy = random.choice(enemies)
    enemy.HP = enemy.MaxHP  # 确保每次战斗开始时敌人的血量是满的
    enemy.MP = enemy.MaxMP  # 同时恢复敌人的魔法值
    return enemy

def choose_class():
    classes = load_classes()
    print("选择你的职业:")
    for key, char in classes.items():
        print(f"{key}: {char.name} (MaxHP: {char.MaxHP}, MaxMP: {char.MaxMP}, ATK: {char.ATK}, DEF: {char.DEF}, MAT: {char.MAT}, MDF: {char.MDF}, AGI: {char.AGI}, LUK: {char.LUK}, 技能: {char.skill})")

    choice = input("请输入对应的数字: ")
    if choice in classes:
        clear_screen()
        return classes[choice]
    else:
        clear_screen()
        print("无效的职业选择，默认选择战士。")
        return classes.get("1")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("欢迎来到文字RPG冒险！")
    player = choose_class()
    print(f"你选择了 {player.name}，冒险开始！")

    # 加载武器和护甲
    weapons = load_weapons()
    armors = load_armor()

    while player.HP > 0:
        print(f"\n当前金币: {player.gold}")
        print(f"HP: {player.HP}/{player.MaxHP}")
        print(f"MP: {player.MP}/{player.MaxMP}")
        print(f"EXP: {player.exp}/{player.exp_to_next}")
        print(f"暴击率: {player.LUK/2}%")
        print(f"武器: {player.weapon}")

        if player.equipment:
            print("护甲: " + ", ".join(str(item) for item in player.equipment))
        else:
            print("护甲: None")

        command = input("输入 'q' 退出游戏, 按 Enter 继续战斗: ")
        if command.lower() == 'q':
            print("游戏结束，再见！")
            break
        battle(player)
        if player.HP > 0:
            player.HP = min(player.MaxHP, player.HP + int(player.MaxHP*0.25))
            player.MP = min(player.MaxMP, player.MP + int(player.MaxMP*0.25))
            print("你恢复了一部分生命值和魔法值，准备迎接下一个挑战！")

if __name__ == "__main__":
    main()