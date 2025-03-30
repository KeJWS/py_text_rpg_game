import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_equipment(player):
    """显示玩家当前装备"""
    weapon_info = f"{player.weapon.name} (ATK+{player.weapon.attack_bonus})" if player.weapon else "无"
    armor_info = f"{player.equipment.name} (DEF+{player.equipment.defense_bonus}, HP+{player.equipment.health_bonus})" if player.equipment else "无"

    print("\n🔹 当前装备:")
    print(f"    🔪 武器: {weapon_info}")
    print(f"    🛡️ 护甲: {armor_info}")

def select_equipment(equipment_dict, equipment_type):
    """通过 ID 选择装备"""
    print(f"\n可选{equipment_type}：")
    for eq_id, item in equipment_dict.items():
        if equipment_type == "武器":
            print(f"{eq_id}: {item.name} (ATK+{item.attack_bonus})")
        else:
            print(f"{eq_id}: {item.name} (DEF+{item.defense_bonus}, HP+{item.health_bonus})")

    choice = input(f"\n请输入{equipment_type}ID (输入 0 取消): ")
    clear_screen()
    
    if choice.isdigit():
        choice_id = int(choice)
        return equipment_dict.get(choice_id, None) if choice_id != 0 else None
    else:
        print("⚠️ 无效的输入，请输入正确的 ID！")
        return None

def change_equipment(player, weapons, armors):
    """玩家换装交互菜单"""
    while True:
        # clear_screen()
        display_equipment(player)

        print("\n🎭 请选择装备操作：")
        print("1️⃣ 更换武器")
        print("2️⃣ 更换护甲")
        print("3️⃣ 脱下武器")
        print("4️⃣ 脱下护甲")
        print("5️⃣ 脱下所有装备")
        print("0️⃣ 返回游戏\n")

        choice = input("请输入你的选择，Enter 返回游戏: ")

        if choice == "1":
            weapon = select_equipment(weapons, "武器")
            if weapon:
                player.equip_weapon(weapon)
                print(f"✅ 你装备了 {weapon.name} (ATK+{weapon.attack_bonus})")
            else:
                print("⚠️ 未更换武器。")
        elif choice == "2":
            armor = select_equipment(armors, "护甲")
            if armor:
                player.equip_armor(armor)
                print(f"✅ 你装备了 {armor.name} (DEF+{armor.defense_bonus}, HP+{armor.health_bonus})")
            else:
                print("⚠️ 未更换护甲。")
        elif choice == "3":
            if player.weapon:
                clear_screen()
                print(f"❌ 你脱下了 {player.weapon.name}。")
                player.equip_weapon(None)
            else:
                print("⚠️ 你没有装备武器。")
        elif choice == "4":
            if player.equipment:
                clear_screen()
                print(f"❌ 你脱下了 {player.equipment.name}。")
                player.equip_armor(None)
            else:
                print("⚠️ 你没有装备护甲。")
        elif choice == "5":
            if player.weapon or player.equipment:
                clear_screen()
                print("❌ 你脱下了所有装备。")
                player.equip_weapon(None)
                player.equip_armor(None)
            else:
                print("⚠️ 你已经没有装备。")
        else:
            clear_screen()
            break