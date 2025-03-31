def main():
    print("欢迎来到文字RPG冒险！")
    
    player, weapon_id, armor_id = choose_class()  # 获取职业 & 装备 ID
    items = load_items()
    weapons = load_weapons()
    armors = load_armor()

    item_shop = ItemShop(items)
    weapon_shop = WeaponShop(weapons)
    armor_shop = ArmorShop(armors)

    # 🎁 给予玩家初始武器和护甲
    player.weapon = weapons.get(weapon_id, None)
    player.equipment = armors.get(armor_id, None)

    print(f"🎁 你获得了初始装备: {player.weapon.name} 和 {player.equipment.name}！")

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
