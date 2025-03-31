def drop_rewards(self):
    """敌人死亡后掉落奖励"""
    import random

    items = load_items()
    weapons = load_weapons()
    armors = load_armor()

    drop_chance = random.random()  # 生成0-1之间的随机数

    if drop_chance < 0.5:  # 50% 概率掉落普通物品
        item_id = random.choice(list(items.keys()))
        item = items[item_id]  # 获取物品对象
        self.player.inventory.add_item(item, 1)  # 传递物品对象
        print(f"🛍️ 你获得了物品：{item.name}！")

    if drop_chance < 0.3:  # 30% 概率掉落武器
        weapon_id = random.choice(list(weapons.keys()))
        weapon = weapons[weapon_id]  # 获取武器对象
        self.player.weapons[weapon_id] = weapon
        print(f"⚔️ 你获得了武器：{weapon.name}！")

    if drop_chance < 0.2:  # 20% 概率掉落护甲
        armor_id = random.choice(list(armors.keys()))
        armor = armors[armor_id]  # 获取防具对象
        self.player.armors[armor_id] = armor
        print(f"🛡️ 你获得了防具：{armor.name}！")
