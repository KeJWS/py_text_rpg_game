import csv
from character import Character, Enemy

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
                    row['skill']
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
