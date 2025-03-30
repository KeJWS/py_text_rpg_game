import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_equipment(player):
    """显示玩家当前装备"""
    print(f"\n当前装备：\n武器: {player.weapon or '无'}\n护甲: {player.equipment or '无'}")

def select_equipment(equipment_dict, equipment_type):
    """通用装备选择逻辑"""
    print(f"选择{equipment_type}：")
    for key, item in equipment_dict.items():
        print(f"{key}: {item}")

    choice = input(f"请输入{equipment_type}名称: ")
    return equipment_dict.get(choice, None)

def change_equipment(player, weapons, armors):
    """玩家换装交互菜单"""
    while True:
        # clear_screen()
        display_equipment(player)

        print("\n你可以选择换装备：")
        print("1: 更换武器")
        print("2: 更换护甲")
        print("3: 脱下武器")
        print("4: 脱下护甲")
        print("5: 脱下所有装备")

        choice = input("请输入你的选择，Enter 返回游戏: ")

        if choice == "1":
            weapon = select_equipment(weapons, "武器")
            clear_screen()
            player.equip_weapon(weapon) if weapon else print("⚠️ 无效的选择，未更换武器。")
        elif choice == "2":
            armor = select_equipment(armors, "护甲")
            clear_screen()
            player.equip_armor(armor) if armor else print("⚠️ 无效的选择，未更换护甲。")
        elif choice == "3":
            clear_screen()
            player.equip_weapon(None)
        elif choice == "4":
            clear_screen()
            player.equip_armor(None)
        elif choice == "5":
            clear_screen()
            player.equip_weapon(None)
            player.equip_armor(None)
        else:
            clear_screen()
            break