import csv

def load_weapons():
    """从CSV文件加载武器数据"""
    weapons = {}
    with open("weapon.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            weapons[int(row["id"])] = {"name": row["name"], "attack_bonus": int(row["attack_bonus"])}
    return weapons

def load_armor():
    """从CSV文件加载护甲数据"""
    armors = {}
    with open("armor.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            armors[int(row["id"])] = {
                "name": row["name"],
                "defense_bonus": int(row["defense_bonus"]),
                "health_bonus": int(row["health_bonus"]),
            }
    return armors
