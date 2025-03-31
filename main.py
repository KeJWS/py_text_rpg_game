import random
import os
from game_data import load_classes, load_enemies, load_weapons, load_armor, load_items
from character import ItemShop, WeaponShop, ArmorShop, Weapon, Equipment
from change_equipment import change_equipment
from battle import Battle

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_class():
    classes = load_classes()

    # 🎯 各职业初始装备ID（武器ID, 护甲ID）
    initial_equipment = {
        "1": (1, 3),  # 战士: 木剑 + 皮甲
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
    weapon_id, armor_id = initial_equipment.get(choice, (1, 3))  # 获取装备 ID

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
    player.gain_gold(100)
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
