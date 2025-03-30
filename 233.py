import csv
from character import Character, Enemy, Weapon, Equipment, Item, Inventory

def load_csv_data(filename, object_class, field_mapping):
    """
    通用 CSV 解析函数，将 CSV 数据加载为指定类的对象。
    :param filename: CSV 文件名
    :param object_class: 目标类
    :param field_mapping: 字段映射，字典格式 {csv字段: 类属性}
    :return: 字典或列表，取决于 object_class
    """
    data = {} if object_class in [Weapon, Equipment, Item] else []
    
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed_row = {attr: parse_type(row[csv_field]) for csv_field, (attr, parse_type) in field_mapping.items()}
                obj = object_class(**parsed_row)
                if isinstance(data, dict):
                    data[parsed_row['name']] = obj  # 以名称作为键存储
                else:
                    data.append(obj)  # 以列表存储
    except FileNotFoundError:
        print(f"⚠️ 文件 {filename} 未找到！")
    except Exception as e:
        print(f"❌ 读取 {filename} 时出错: {e}")
    
    return data

def parse_enemy_level(level_range):
    """解析敌人的等级范围"""
    min_level, max_level = map(int, level_range.split("-"))
    return min_level, max_level

def load_classes():
    """加载职业数据"""
    field_mapping = {
        'id': ('id', str), 'name': ('name', str), 'max_hp': ('MaxHP', int),
        'max_mp': ('MaxMP', int), 'atk': ('ATK', int), 'defense': ('DEF', int),
        'mat': ('MAT', int), 'mdf': ('MDF', int), 'agi': ('AGI', int),
        'luk': ('LUK', int), 'skill': ('skill', str)
    }
    return load_csv_data('classes.csv', Character, field_mapping)

def load_enemies():
    """加载敌人数据"""
    field_mapping = {
        'name': ('name', str), 'max_hp': ('MaxHP', int), 'max_mp': ('MaxMP', int),
        'atk': ('ATK', int), 'defense': ('DEF', int), 'mat': ('MAT', int),
        'mdf': ('MDF', int), 'agi': ('AGI', int), 'luk': ('LUK', int),
        'skill': ('skill', str), 'exp_reward': ('exp_reward', int),
        'gold_reward': ('gold_reward', int), 'level_range': ('level_range', parse_enemy_level)
    }
    enemies = load_csv_data("enemies.csv", Enemy, field_mapping)
    
    # 解析等级范围
    for enemy in enemies:
        enemy.min_level, enemy.max_level = enemy.level_range
    return enemies

def load_weapons():
    """加载武器数据"""
    field_mapping = {'name': ('name', str), 'attack_bonus': ('attack_bonus', int)}
    return load_csv_data("weapons.csv", Weapon, field_mapping)

def load_armor():
    """加载护甲数据"""
    field_mapping = {
        'name': ('name', str), 'defense_bonus': ('defense_bonus', int), 'health_bonus': ('health_bonus', int)
    }
    return load_csv_data("armor.csv", Equipment, field_mapping)

def load_items():
    """加载道具数据"""
    field_mapping = {
        'id': ('id', str), 'name': ('name', str), 'description': ('description', str),
        'effect': ('effect', str), 'price': ('price', int)
    }
    return load_csv_data("items.csv", Item, field_mapping)
