def change_equipment(player, weapons, armors):
    """让玩家换装备"""
    print("\n当前装备：")
    print(f"武器: {player.weapon}")
    print(f"护甲: {player.equipment}")

    print("\n你可以选择换装备：")
    print("1: 更换武器")
    print("2: 更换护甲")
    print("3: 脱下武器")
    print("4: 脱下护甲")
    print("5: 脱下所有")

    choice = input("请输入你的选择，默认不更换: ")

    if choice == "1":
        print("选择武器：")
        for key, weapon in weapons.items():
            print(f"{key}: {weapon}")
        weapon_choice = input("请输入武器名称: ")
        weapon = weapons.get(weapon_choice, None)
        if weapon:
            player.equip_weapon(weapon)
        else:
            print("无效的武器选择，默认选择长剑。")
            player.equip_weapon(weapons.get("长剑"))

    elif choice == "2":
        print("选择护甲：")
        for key, armor in armors.items():
            print(f"{key}: {armor}")
        armor_choice = input("请输入护甲名称: ")
        armor = armors.get(armor_choice, None)
        if armor:
            player.equip_armor(armor)
        else:
            print("无效的护甲选择，默认选择铁甲。")
            player.equip_armor(armors.get("铁甲"))

    elif choice == "3":
        player.equip_weapon(None)

    elif choice == "4":
        player.equip_armor(None)

    elif choice == "5":
        player.equip_weapon(None)
        player.equip_armor(None)

    else:
        print("未做更换。")
