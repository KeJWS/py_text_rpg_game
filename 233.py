import csv
from character import Weapon, Equipment, Character

def load_classes(filename="classes.csv"):
    classes = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            max_hp = int(row['max_hp'])
            max_mp = int(row['max_mp'])
            atk = int(row['atk'])
            defense = int(row['defense'])
            mat = int(row['mat'])
            mdf = int(row['mdf'])
            agi = int(row['agi'])
            luk = int(row['luk'])
            skill = row['skill']
            weapon_name = row['weapon']
            armor_name = row['armor']
            
            # 创建类并分配武器和护甲
            character = Character(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
            character.weapon = Weapon(weapon_name, atk)  # 根据武器名称创建武器
            character.equipment = [Equipment(armor_name, defense, max_hp * 0.2)]  # 根据护甲名称创建护甲
            
            classes[name] = character
    return classes
