import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combatants = [player, enemy]
        self.status_effects = {player.name: {}, enemy.name: {}}
        self.turn_order = self.get_battle_order()
        self.turn_count = 1

    def get_battle_order(self):
        """排序：敏捷高者先行动，敏捷相同玩家优先"""
        return sorted(self.combatants, key=lambda char: (-char.AGI, char.name == self.player.name))

    def apply_status_effects(self, character):
        """处理状态效果（如中毒、眩晕）"""
        effects = self.status_effects[character.name]
        if 'poison' in effects:
            poison_damage = max(1, character.MaxHP // 10)
            character.HP -= poison_damage
            print(f"{character.name} 受到中毒影响，损失 {poison_damage} HP！")
        if 'stun' in effects:
            print(f"{character.name} 被眩晕，无法行动！")
            return False  
        return True

    def player_action(self):
        action = input("选择行动 (a. 攻击 s. 技能 q. 逃跑 d. 防御): ")
        if action == "a":
            self.player.attack(self.enemy)
        elif action == "s":
            if not self.player.use_skill(self.enemy):
                return False 
        elif action == "q":
            if self.try_escape():
                return True
        elif action == "d":
            self.status_effects[self.player.name]['defend'] = True
            print("🛡️ 你进入防御状态，伤害减少 50%！")
        else:
            # print("⚠️ 无效选择，默认攻击！")
            self.player.attack(self.enemy)
        return False

    def enemy_action(self, enemy):
        """敌人行为逻辑
        if enemy.HP < enemy.MaxHP * 0.3 and random.random() < 0.3:
            print(f"{enemy.name} 进入防御状态！")
            self.status_effects[enemy.name]['defend'] = True
            return
        """
        damage = enemy.calculate_damage(self.player)
        if 'defend' in self.status_effects[self.player.name]:
            damage //= 2
            print(f"🛡️ 你成功防御，伤害减少为 {damage}！")
        self.player.HP -= damage
        print(f"🔥 {enemy.name} 攻击了你，造成 \033[33m{damage}\033[0m 伤害！")

    def try_escape(self):
        escape_chance = min(90, max(10, self.player.AGI * 3))  # 逃跑概率：10% - 90%
        if random.randint(1, 100) <= escape_chance:
            print("🏃 你成功逃跑了！")
            input("\n按 Enter 继续...")
            return True
        else:
            print(f"🚫 {self.enemy.name} 阻止了你的逃跑！")
            return False

    def process_battle(self):
        print(f"\n⚔️ 你遇到了 {self.enemy.name}！⚔️")
        while self.player.HP > 0 and self.enemy.HP > 0:
            print(f"\n==== 🌀 第 {self.turn_count} 回合 ====")
            print(f"💖 你的生命值: \033[31m{self.player.HP}/{self.player.MaxHP}\033[0m | MP: {self.player.MP}/{self.player.MaxMP}")
            print(f"💀 {self.enemy.name} 生命值: \033[32m{self.enemy.HP}/{self.enemy.MaxHP}\033[0m")
            # print("🔄 行动顺序:", " -> ".join([c.name for c in self.turn_order]))
            print()

            for combatant in self.turn_order:
                if combatant.HP <= 0:
                    continue
                if not self.apply_status_effects(combatant):
                    continue  # 若被眩晕，跳过回合
                if combatant == self.player:
                    if self.player_action():
                        return
                else:
                    self.enemy_action(combatant)
            # 清除单回合状态
            for combatant in self.combatants:
                self.status_effects[combatant.name].pop('defend', None)
            self.turn_count += 1  # 进入下一回合

        self.battle_result()

    def battle_result(self):
        if self.player.HP > 0:
            print(f"🏆 你击败了 {self.enemy.name}！")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gain_gold(self.enemy.gold_reward)
            print(f"\033[31mHP: {self.player.HP}/{self.player.MaxHP}\033[0m")

        else:
            print("💀 \033[31m你被击败了，游戏结束。\033[0m")

        input("\n按 Enter 继续...")
        clear_screen()
