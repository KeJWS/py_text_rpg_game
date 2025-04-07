import random

prefixes = {
    "破旧的": 0.7,
    "普通的": 1.0,
    "结实的": 1.2,
    "魔法的": 1.5,
    "传奇的": 2.0
}

armor_types = {
    "布衣": {"max_hp": (80, 150), "mat": (5, 10), "mdf": (5, 10), "def": (1, 3)},
    "铁甲": {"def": (5, 10), "health_bonus": (20, 40), "agi": (2, 5)},
    "皮甲": {"agi": (8, 15), "def": (3, 5)},
    "魔法袍": {"max_mp": (30, 60), "mat": (10, 20), "mdf": (8, 15)},
    "重甲": {"def": (10, 20), "max_hp": (200, 400), "mdf": (5, 10)},
}

def generate_armor_stats(base_stats, multiplier):
    stats = {
        "max_hp": 0, "max_mp": 0, "attack_bonus": 0,
        "defense_bonus": 0, "health_bonus": 0,
        "mat": 0, "mdf": 0, "agi": 0, "luk": 0
    }
    for key, (low, high) in base_stats.items():
        val = int(random.randint(low, high) * multiplier)
        if key == "def":
            stats["defense_bonus"] = val
        else:
            stats[key] = val
    return stats

def generate_armor(id):
    prefix, multiplier = random.choice(list(prefixes.items()))
    base_name = random.choice(list(armor_types.keys()))
    full_name = prefix + base_name
    base_stats = armor_types[base_name]
    stats = generate_armor_stats(base_stats, multiplier)
    
    # price = 简化计算：各属性加权总和
    price = sum([
        stats["max_hp"] // 10,
        stats["max_mp"] // 10,
        stats["attack_bonus"] * 5,
        stats["defense_bonus"] * 10,
        stats["health_bonus"],
        stats["mat"] * 6,
        stats["mdf"] * 5,
        stats["agi"] * 4,
        stats["luk"] * 3
    ])
    
    note = 0
    return f'{id},{full_name},{stats["max_hp"]},{stats["max_mp"]},{stats["attack_bonus"]},{stats["defense_bonus"]},{stats["health_bonus"]},{stats["mat"]},{stats["mdf"]},{stats["agi"]},{stats["luk"]},{price},{note}'

def generate_armor_list(count=10):
    lines = ["id,name,max_hp,max_mp,attack_bonus,defense_bonus,health_bonus,mat,mdf,agi,luk,price,note"]
    for i in range(1, count + 1):
        lines.append(generate_armor(i))
    return "\n".join(lines)

# 示例输出
armor_csv = generate_armor_list(99)
print(armor_csv)
