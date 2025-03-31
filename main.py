import random
import os
from game_data import load_classes, load_enemies, load_weapons, load_armor, load_items
from character import ItemShop, WeaponShop, ArmorShop, Weapon, Equipment
from change_equipment import change_equipment

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combatants = [player, enemy]
        self.status_effects = {player.name: {}, enemy.name: {}}
        self.turn_order = self.get_battle_order()
        self.turn_count = 1  # 新增回合计数

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
            print("🛡️ 你进入防御状态，本回合受到的伤害减少 50%！")
        else:
            print("⚠️ 无效的选择，默认进行普通攻击！")
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
            damage //= 2  # 玩家防御时伤害减少50%
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
            print(f"💀 {self.enemy.name} 的生命值: \033[32m{self.enemy.HP}/{self.enemy.MaxHP}\033[0m | MP: {self.enemy.MP}/{self.enemy.MaxMP}")
            print("🔄 行动顺序:", " -> ".join([c.name for c in self.turn_order]))
            print()

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
            self.turn_count += 1  # 进入下一回合

        self.battle_result()

    def battle_result(self):
        if self.player.HP > 0:
            print(f"🏆 你击败了 {self.enemy.name}！")
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gain_gold(self.enemy.gold_reward)
        else:
            print("💀 \033[31m你被击败了，游戏结束。\033[0m")

        input("\n按 Enter 继续...")
        clear_screen()

def choose_class():
    classes = load_classes()

    # 🎯 各职业初始装备ID（武器ID, 护甲ID）
    initial_equipment = {
        "1": (1, 3),  # 战士: 木剑 + 皮甲甲
        "2": (2, 1),  # 法师: 木杖 + 布衣
        "3": (3, 1),  # 盗贼: 匕首 + 布衣
        "4": (4, 3)   # 勇者: 勇者剑 + 皮甲
    }

    print("选择你的职业:")
    # for key, char in classes.items():
        # print(f"{key}: {char.name} (MaxHP: {char.MaxHP}, MaxMP: {char.MaxMP}, ATK: {char.ATK}, DEF: {char.DEF}, MAT: {char.MAT}, MDF: {char.MDF}, AGI: {char.AGI}, LUK: {char.LUK}, 技能: {char.skill})")

    print("1、战士，注重攻击和防御。\n2、法师，注重魔攻和魔防。\n3、盗贼，更高的敏捷和运气。\n4、勇者，感觉是个厉害的角色。")

    choice = input("请输入对应的数字: ")
    clear_screen()
    chosen_class = classes.get(choice, classes["1"])
    weapon_id, armor_id = initial_equipment.get(choice, (1, 1))  # 获取装备 ID

    return chosen_class, weapon_id, armor_id  # 返回职业 + 装备 ID

def get_random_enemy(player_level):
    """根据玩家等级随机选择合适的敌人"""
    enemies = load_enemies()
    available_enemies = [e for e in enemies if e.min_level <= player_level <= e.max_level]
    enemy = random.choice(available_enemies) if available_enemies else min(enemies, key=lambda e: e.min_level)  # 返回最低等级敌人，避免错误
    enemy.HP, enemy.MP = enemy.MaxHP, enemy.MaxMP
    return enemy

def battle(player):
    enemy = get_random_enemy(player.level)
    battle_instance = Battle(player, enemy)
    battle_instance.process_battle()

def external_change_equipment(player):
    clear_screen()
    print("更换装备")
    change_equipment(player)

def shop_menu(player, shop):
    while True:
        shop.display_items()
        print(f"\n💰 你的金币: {player.gold} G")
        item_id = input("🔹 请输入要购买的物品 ID（输入 q 退出）: ")
        if item_id == "q":
            clear_screen()
            break
        if item_id.isdigit():
            clear_screen()
            shop.buy_item(player, int(item_id))
        else:
            clear_screen()
            print("⚠️ 请输入正确的物品 ID！")

def display_player_info(player):
    """显示玩家当前状态"""
    print(f"\n{player.name} (LV: {player.level})")
    print(f"\033[31mHP: {player.HP}/{player.MaxHP}\033[0m  MP: {player.MP}/{player.MaxMP}")
    print(f"EXP: {player.exp}/{player.exp_to_next}  |  💰 \033[33m金币: {player.gold} G\033[0m")
    print(f"ATK: {player.ATK}   DEF: {player.DEF}   MAT: {player.MAT}   MDF: {player.MDF}")
    print(f"AGI: {player.AGI}   LUK: {player.LUK}")
    print(f"暴击率: {player.LUK/2}%")
    print(f"🔪 武器: {player.weapon}")
    print(f"🛡️ 护甲: {player.equipment}")

def main():
    print("欢迎来到文字RPG冒险！")
    player, weapon_id, armor_id = choose_class()  # 获取职业 & 装备 ID
    items = load_items()
    weapons = load_weapons()
    armors = load_armor()

    item_shop = ItemShop(items)
    weapon_shop = WeaponShop(weapons)
    armor_shop = ArmorShop(armors)

    print(f"🎁 你获得了初始装备！")
    player.add_weapon(weapons[weapon_id])
    player.add_armor(armors[armor_id])

    print(f"你选择了 {player.name}，冒险开始！")

    while player.HP > 0:
        display_player_info(player)

        print()
        command = input("e: 退出, w: 换装, b: 背包, m: 商店, a: 战斗 ")
        if command.lower() == 'e':
            print("游戏结束，再见！")
            break

        elif command.lower() == 'w':
            external_change_equipment(player)

        elif command == "b":
            clear_screen()
            while True:
                print(f"{player.name}")
                print(f"\033[31mHP: {player.HP}/{player.MaxHP}\033[0m  MP: {player.MP}/{player.MaxMP}")
                player.inventory.view_inventory(items)
                use_command = input("输入物品 ID 以使用, 或输入 q 退出: ")
                if use_command == "q":
                    break
                elif use_command.isdigit() and int(use_command) in items:
                    player.inventory.use_item(int(use_command), player, items)
                input("\n按 Enter 继续...")
                clear_screen()

        elif command == "m":
            clear_screen()
            while True:
                print("\n🏪 欢迎来到商店区！你想进入哪个商店？")
                print("1. 物品商店")
                print("2. 武器商店")
                print("3. 护甲商店")
                choice = input("输入选项，q 退出: ")

                if choice == "1":
                    clear_screen()
                    shop_menu(player, item_shop)
                elif choice == "2":
                    clear_screen()
                    shop_menu(player, weapon_shop)
                elif choice == "3":
                    clear_screen()
                    shop_menu(player, armor_shop)
                elif choice == "q":
                    clear_screen()
                    print("👋 再见，欢迎下次光临！")
                    break
                else:
                    clear_screen()
                    print("⚠️ 请输入有效选项！")

        elif command == "a":
            clear_screen()
            battle(player)
            if player.HP > 0:
                player.HP = min(player.MaxHP, player.HP + int(player.MaxHP*0.25))
                player.MP = min(player.MaxMP, player.MP + int(player.MaxMP*0.25))
                print("你恢复了一部分生命值和魔法值，准备迎接下一个挑战！")
                input("\n按 Enter 继续...")

        clear_screen()
        print("干嘛呢？")

if __name__ == "__main__":
    main()
