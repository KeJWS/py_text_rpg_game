import random

prefixes = {
    "破损的": 0.7,
    "普通的": 1.0,
    "锐利的": 1.2,
    "精良的": 1.5,
    "传奇的": 2.0
}

weapon_types = {
    "木剑": {"atk": (4, 7)},
    "木杖": {"mat": (4, 8)},
    "小刀": {"agi": (8, 15)},
    "勇者剑": {"atk": (10, 20), "def": (10, 20), "mat": (10, 20), "mdf": (10, 20), "agi": (10, 20), "luk": (10, 20)},
    "弓": {"agi": (10, 20), "atk": (8, 12)},
    "大锤": {"atk": (15, 25), "def": (10, 25)},
    "法杖": {"mat": (20, 40), "mdf": (10, 20)},
    "匕首": {"agi": (15, 25), "luk": (5, 10)},
    "钢剑": {"atk": (12, 18), "def": (6, 12)}
}

def generate_weapon_stats(base_stats, multiplier):
    stats = {
        "max_hp": random.randint(50, 300),
        "max_mp": random.randint(10, 100),
        "attack_bonus": 0,
        "defense": 0,
        "mat": 0,
        "mdf": 0,
        "agi": 0,
        "luk": 0
    }

    for key, (low, high) in base_stats.items():
        stats[key if key != "atk" else "attack_bonus"] = int(random.randint(low, high) * multiplier)
    
    return stats

def generate_weapon(id):
    prefix, multiplier = random.choice(list(prefixes.items()))
    base_name = random.choice(list(weapon_types.keys()))
    full_name = prefix + base_name
    base_stats = weapon_types[base_name]
    stats = generate_weapon_stats(base_stats, multiplier)
    
    price = sum([
        stats["attack_bonus"] * 5,
        stats["defense"] * 4,
        stats["mat"] * 5,
        stats["mdf"] * 4,
        stats["agi"] * 3,
        stats["luk"] * 2,
        stats["max_hp"] // 10,
        stats["max_mp"] // 5
    ])
    
    note = 0
    return f'{id},{full_name},{stats["max_hp"]},{stats["max_mp"]},{stats["attack_bonus"]},{stats["defense"]},{stats["mat"]},{stats["mdf"]},{stats["agi"]},{stats["luk"]},{price},{note}'

def generate_weapon_list(count=10):
    lines = ["id,name,max_hp,max_mp,attack_bonus,defense,mat,mdf,agi,luk,price,New Column,note"]
    for i in range(1, count + 1):
        lines.append(generate_weapon(i))
    return "\n".join(lines)

# 运行示例
weapon_csv = generate_weapon_list(99)
print(weapon_csv)
