import csv
from character import Character, Enemy, Weapon, Equipment, Item, Inventory

def load_classes():
    """从 CSV 加载职业数据，返回字典"""
    classes = {}
    try:
        with open('classes.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                classes[row['id']] = Character(
                    row['name'],
                    int(row['max_hp']), int(row['max_mp']), int(row['atk']), int(row['defense']),
                    int(row['mat']), int(row['mdf']), int(row['agi']), int(row['luk']),
                    row['skill'],
                )
    except FileNotFoundError:
        print("❌ 职业数据文件 classes.csv 未找到！")
        exit()
    except Exception as e:
        print(f"❌ 读取 classes.csv 时出错: {e}")
        exit()
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
    try:
        with open("enemies.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                min_level, max_level = parse_enemy_level(row["level_range"])
                enemies.append(Enemy(
                    name=row["name"],
                    max_hp=int(row["max_hp"]),
                    max_mp=int(row["max_mp"]),
                    atk=int(row["atk"]),
                    defense=int(row["defense"]),
                    mat=int(row["mat"]),
                    mdf=int(row["mdf"]),
                    agi=int(row["agi"]),
                    luk=int(row["luk"]),
                    skill=row["skill"],
                    exp_reward=int(row["exp_reward"]),
                    gold_reward=int(row["gold_reward"]),
                    min_level=min_level,
                    max_level=max_level
                ))
    except FileNotFoundError:
        print("❌ 敌人数据文件 enemies.csv 未找到！")
        exit()
    except Exception as e:
        print(f"❌ 读取 enemies.csv 时出错: {e}")
        exit()
    return enemies

def load_weapons(filename="weapons.csv"):
    weapons = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            attack_bonus = int(row['attack_bonus'])
            weapons[name] = Weapon(name, attack_bonus)
    return weapons

def load_armor(filename="armor.csv"):
    armors = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            defense_bonus = int(row['defense_bonus'])
            health_bonus = int(row['health_bonus'])
            armors[name] = Equipment(name, defense_bonus, health_bonus)
    return armors

def load_items():
    items = {}
    with open("items.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            item = Item(*row)
            items[item.id] = item
        return items
