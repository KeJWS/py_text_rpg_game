import csv
from character import Character, Enemy, Weapon, Equipment

def load_classes():
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
        print("职业数据文件未找到！")
        exit()
    except Exception as e:
        print(f"读取职业数据时出错: {e}")
        exit()
    return classes

def load_enemies():
    enemies = []
    try:
        with open('enemies.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                enemies.append(Enemy(
                    row['name'],
                    int(row['max_hp']), int(row['max_mp']), int(row['atk']), int(row['defense']),
                    int(row['mat']), int(row['mdf']), int(row['agi']), int(row['luk']),
                    row['skill'],
                    int(row['exp_reward']),
                    int(row['gold_reward'])
                ))
    except FileNotFoundError:
        print("敌人数据文件未找到！")
        exit()
    except Exception as e:
        print(f"读取敌人数据时出错: {e}")
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