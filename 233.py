import csv
import random
import os
from game_data import load_classes, load_enemies, load_weapons, load_armor
from character import Character, Enemy, Weapon, Equipment

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combatants = [player, enemy]
        self.status_effects = {player.name: {}, enemy.name: {}}
        self.turn_order = self.get_battle_order()

    def get_battle_order(self):
        """根据敏捷（AGI）排序，敏捷高的角色先行动，若敏捷相同，玩家优先"""
        return sorted(self.combatants, key=lambda char: (-char.AGI, char.name == self.player.name))

    def apply_status_effects(self, character):
        """处理回合开始时的状态效果，如中毒、眩晕等"""
        effects = self.status_effects[character.name]
        if 'poison' in effects:
            poison_damage = max(1, character.MaxHP // 10)
            character.HP -= poison_damage
            print(f"{character.name} 受到中毒影响，损失 {poison_damage} HP！")
        if 'stun' in effects:
            print(f"{character.name} 被眩晕，无法行动！")
            return False  # 被眩晕跳过回合
        return True

    def player_action(self):
        action = input("选择行动 (a. 攻击 s. 使用技能 q. 逃跑 d. 防御): ")
        if action == "a":
            self.player.attack(self.enemy)
        elif action == "s":
            if not self.player.use_skill(self.enemy):
                return False  # 取消行动
        elif action == "q":
            if self.try_escape():
                return True  # 逃跑成功
        elif action == "d":
            self.status_effects[self.player.name]['defend'] = True
            print("你进入防御状态，本回合受到的伤害减少50%！")
        else:
            print("无效的选择，默认攻击！")
            self.player.attack(self.enemy)
        return False

    def enemy_action(self, enemy):
        """敌人行为逻辑"""
        if enemy.HP < enemy.MaxHP * 0.3 and random.random() < 0.3:
            print(f"{enemy.name} 进入防御状态！")
            self.status_effects[enemy.name]['defend'] = True
            return
        damage = enemy.calculate_damage(self.player)
        if 'defend' in self.status_effects[self.player.name]:
            damage //= 2  # 玩家防御时伤害减少50%
        self.player.HP -= damage
        print(f"{enemy.name} 攻击了你，造成 {damage} 伤害！")

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
                if not self.apply_status_effects(combatant):
                    continue  # 若被眩晕，跳过回合
                if combatant == self.player:
                    if self.player_action():
                        return  # 逃跑成功，结束战斗
                else:
                    self.enemy_action(combatant)
            # 清除单回合状态
            for combatant in self.combatants:
                self.status_effects[combatant.name].pop('defend', None)
        self.battle_result()

    def battle_result(self):
        if self.player.HP > 0:
            print(f"你击败了 {self.enemy.name}！")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gain_gold(self.enemy.gold_reward)
        else:
            print("你被击败了，游戏结束。")
        input("\n按 Enter 继续...")
