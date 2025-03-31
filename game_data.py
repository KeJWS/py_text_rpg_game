import csv
from character import Character, Enemy, Weapon, Equipment, Item, Inventory, Map

def load_classes():
    """从 CSV 加载职业数据，返回字典"""
    classes = {}
    with open('classes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            classes[row['id']] = Character(
                row['name'],
                int(row['max_hp']), int(row['max_mp']), int(row['atk']), int(row['defense']),
                int(row['mat']), int(row['mdf']), int(row['agi']), int(row['luk']),
                row['skill'],
            )
    return classes

def parse_enemy_level(level_range):
    """解析敌人的等级范围，如 '1-3' 解析为 (1, 3)"""
    try:
        min_level, max_level = map(int, level_range.split("-"))
        return min_level, max_level
    except ValueError:
        print(f"⚠️ 无效的等级范围: {level_range}，使用默认值 (1, 1)")
        return 1, 1

def load_enemies():
    """从 CSV 加载敌人数据，返回列表"""
    enemies = []
    with open("enemies.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            min_level, max_level = parse_enemy_level(row["level_range"])
            enemies.append(Enemy(
                id=int(row["id"]), name=row["name"],
                max_hp=int(row["max_hp"]), max_mp=int(row["max_mp"]),
                atk=int(row["atk"]), defense=int(row["defense"]),
                mat=int(row["mat"]), mdf=int(row["mdf"]),
                agi=int(row["agi"]), luk=int(row["luk"]),
                skill=row["skill"],
                exp_reward=int(row["exp_reward"]),
                gold_reward=int(row["gold_reward"]),
                min_level=min_level,
                max_level=max_level
            ))
    return enemies

def load_items():
    items = {}
    with open("items.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            items[int(row["id"])] = Item(int(row["id"]), row["name"], row["type"], row["effect"], int(row["value"]), int(row["price"]), int(row["note"]))
    return items

def load_weapons():
    weapons = {}
    with open('weapons.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            weapon = Weapon(
                id=int(row['id']),
                name=row['name'],
                attack_bonus=int(row['attack_bonus']),
                price=int(row['price']),
                note=int(row['note']),
            )
            weapons[weapon.id] = weapon
    return weapons

def load_armor():
    armors = {}
    with open('armor.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            armor = Equipment(
                id=int(row['id']),
                name=row['name'],
                defense_bonus=int(row['defense_bonus']),
                health_bonus=int(row['health_bonus']),
                price=int(row['price']),
                note=int(row['note']),
            )
            armors[armor.id] = armor
    return armors

def load_maps():
    """加载地图数据"""
    maps = {
        "1": Map("草原 Lv1", [1, 2, 4]),
        "2": Map("沙漠 Lv3", [3, 4]),
        "3": Map("死亡谷 Lv7", [5, 6, 7]),
    }
    return maps

