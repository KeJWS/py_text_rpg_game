import random
import os
from game_data import load_classes, load_enemies, load_weapons, load_armor, load_items, load_maps
from character import ItemShop, WeaponShop, ArmorShop, Weapon, Equipment
from change_equipment import change_equipment
from battle import Battle

def clear_screen():
    """清除屏幕，兼容 Windows 和 Unix 系统"""
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_class():
    """让玩家选择职业，并返回对应的初始装备 ID"""
    classes = load_classes()
    
    # 各职业初始装备 ID（武器 ID, 护甲 ID）
    initial_equipment = {
        "1": (1, 3),  # 战士
        "2": (2, 1),  # 法师
        "3": (3, 1),  # 盗贼
        "4": (4, 3)   # 勇者
    }
    
    print("选择你的职业:")
    print("1、战士，注重攻击和防御。\n2、法师，注重魔攻和魔防。\n3、盗贼，更高的敏捷和运气。\n4、勇者，感觉是个厉害的角色。")
    
    choice = input("请输入对应的数字: ")
    clear_screen()
    
    # 获取玩家选择的职业及初始装备 ID
    chosen_class = classes.get(choice, classes["1"])
    weapon_id, armor_id = initial_equipment.get(choice, (1, 3))
    
    return chosen_class, weapon_id, armor_id

def get_random_enemy(player_level):
    """根据玩家等级随机选择合适的敌人"""
    enemies = load_enemies()
    
    # 筛选适合当前玩家等级的敌人
    available_enemies = [e for e in enemies if e.min_level <= player_level <= e.max_level]
    
    # 如果没有合适的敌人，则选择最低等级的敌人，防止报错
    enemy = random.choice(available_enemies) if available_enemies else min(enemies, key=lambda e: e.min_level)
    enemy.HP, enemy.MP = enemy.MaxHP, enemy.MaxMP  # 初始化敌人 HP 和 MP
    return enemy

def battle(player):
    """玩家进入战斗模式，与随机敌人战斗"""
    chosen_map = choose_map()
    while True:
        enemy = chosen_map.get_enemy(player.level)
        
        if not enemy:
            print("⚠️ 这个地图没有适合你当前等级的敌人！")
            break
        
        print(f"你遇到了 {enemy.name}！")
        battle_instance = Battle(player, enemy)
        battle_instance.process_battle()
        
        if player.HP <= 0:
            break
        
        if input("\n继续战斗？(输入 q 退出): ").lower() == "q":
            print("你选择退出刷怪模式，回到主菜单。")
            break
        
        # 战斗结束后恢复部分 HP 和 MP
        player.HP = min(player.MaxHP, player.HP + int(player.MaxHP * 0.25))
        player.MP = min(player.MaxMP, player.MP + int(player.MaxMP * 0.25))
        print("你恢复了一部分生命值和魔法值，准备迎接下一个怪物！")

def external_change_equipment(player):
    """调用装备更换系统"""
    clear_screen()
    print("更换装备")
    change_equipment(player)

def shop_menu(player, shop):
    """商店系统，允许玩家购买物品"""
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
    """显示玩家当前状态，包括属性、装备和金币"""
    print(f"\n{player.name} (LV: {player.level})")
    print(f"\033[31mHP: {player.HP}/{player.MaxHP}\033[0m  MP: {player.MP}/{player.MaxMP}")
    print(f"EXP: {player.exp}/{player.exp_to_next}  |  💰 \033[33m金币: {player.gold} G\033[0m")
    print(f"ATK: {player.ATK}   DEF: {player.DEF}   MAT: {player.MAT}   MDF: {player.MDF}")
    print(f"AGI: {player.AGI}   LUK: {player.LUK}")
    print(f"暴击率: {player.LUK/2}%")
    print(f"🔪 武器: {player.weapon}")
    print(f"🛡️ 护甲: {player.equipment}")

def rebirth(player):
    """转生系统，允许玩家复活并重置属性"""
    print("\n💀 你已死亡！但你可以选择转生继续冒险！")
    choice = input("是否转生？(y/n): ").lower()
    
    if choice == "y":
        if player.weapon or player.equipment:
            print("❌ 你脱下了所有装备。")
            player.equip_weapon(None)
            player.equip_armor(None)
        player.reset_stats()  # 重置玩家属性
        input("\n按 Enter 继续冒险...")
    else:
        print("游戏结束，再见！")
        exit()

def choose_map():
    """让玩家选择冒险地图"""
    maps = load_maps()
    print("选择你的冒险地图:")
    for key, map in maps.items():
        print(f"{key}: {map.name}")
    choice = input("请输入对应的数字: ")
    clear_screen()
    return maps.get(choice, maps["1"])  # 默认返回草原地图

def main():
    """游戏主循环，控制玩家交互"""
    print("欢迎来到文字RPG冒险！")
    player, weapon_id, armor_id = choose_class()
    items, weapons, armors = load_items(), load_weapons(), load_armor()
    
    # 创建商店
    item_shop, weapon_shop, armor_shop = ItemShop(items), WeaponShop(weapons), ArmorShop(armors)
    
    print("🎁 你获得了初始装备！")
    player.gain_gold(100)
    player.add_weapon(weapons[weapon_id])
    player.add_armor(armors[armor_id])
    
    print(f"你选择了 {player.name}，冒险开始！")
    while player.HP > 0:
        display_player_info(player)
        command = input("e: 退出, w: 换装, b: 背包, m: 商店, a: 战斗 ")
        if command.lower() == 'e':
            print("游戏结束，再见！")
            break
        elif command.lower() == 'w':
            external_change_equipment(player)
        elif command == "b":
            clear_screen()
        elif command == "m":
            clear_screen()
        elif command == "a":
            clear_screen()
            battle(player)
if __name__ == "__main__":
    main()
