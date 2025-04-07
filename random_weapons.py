import random

prefixes = {
    "极差的": 0.5,
    "破损的": 0.7,
    "普通的": 1.0,
    "锐利的": 1.2,
    "精良的": 1.5,
    "传奇的": 2.0,
    "超神的": 4.0,
    "灭世的": 10.0
}

weapon_types = {
    "木剑 🗡️": {"atk": (4, 7)},
    "木杖 🏏": {"mat": (4, 8)},
    "小刀 🔪": {"agi": (8, 15)},
    "勇者剑 🗡️": {"atk": (10, 20), "def": (10, 20), "mat": (10, 20), "mdf": (10, 20), "agi": (10, 20), "luk": (10, 20)},
    "弓 🏹": {"agi": (10, 20), "atk": (8, 12)},
    "大锤 🏏": {"atk": (15, 25), "def": (10, 25), "agi": (-10, 1)},
    "法杖 🏏": {"mat": (20, 40), "mdf": (10, 20)},
    "匕首 🔪": {"agi": (15, 25), "luk": (5, 10)},
    "钢剑 🗡️": {"atk": (12, 18), "def": (6, 12)},
    "双手剑 ⚔️": {"atk": (15, 27), "agi": (-5, 1)},
}

level_suffixes = {
    "Lv1": 0.9,
    "Lv2": 1.1,
    "Lv3": 1.2,
    "Lv4": 1.3,
    "Lv5": 1.4,
    "Lv6": 1.5,
    "Lv7": 1.6,
    "Lv8": 1.8,
    "Lv9": 2.5,
    "Lv10": 3.0,
}

def generate_weapon_stats(base_stats, multiplier):
    stats = {
        "max_hp": random.randint(25, 500),
        "max_mp": random.randint(10, 300),
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
    prefix, prefix_multiplier = random.choice(list(prefixes.items()))
    base_name = random.choice(list(weapon_types.keys()))
    base_stats = weapon_types[base_name]
    
    level, level_multiplier = random.choice(list(level_suffixes.items()))
    
    full_name = f"{prefix}{base_name} {level}"
    total_multiplier = prefix_multiplier * level_multiplier
    
    stats = generate_weapon_stats(base_stats, total_multiplier)
    
    price = sum([
        stats["attack_bonus"] * 50,
        stats["defense"] * 30,
        stats["mat"] * 50,
        stats["mdf"] * 30,
        stats["agi"] * 50,
        stats["luk"] * 50,
        stats["max_hp"] // 3,
        stats["max_mp"]
    ])
    
    note = 0
    rate = f"{prefix_multiplier:.1f}x * {level_multiplier:.1f}x"
    return f'{id},{full_name},{stats["max_hp"]},{stats["max_mp"]},{stats["attack_bonus"]},{stats["defense"]},{stats["mat"]},{stats["mdf"]},{stats["agi"]},{stats["luk"]},{price},{note},{rate}'


def generate_weapon_list(count=10):
    lines = ["id,name,max_hp,max_mp,attack_bonus,defense,mat,mdf,agi,luk,price,note,rate"]
    for i in range(1, count + 1):
        lines.append(generate_weapon(i))
    return "\n".join(lines)

# 运行示例
with open("weapons.csv", "w", encoding="utf-8") as f:
    f.write(generate_weapon_list(299))

