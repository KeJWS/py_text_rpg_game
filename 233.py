# 读取敌人数据
enemies = load_enemies()

# 根据难度分类敌人
low_level_enemies = [e for e in enemies if e.level <= 4]
mid_level_enemies = [e for e in enemies if 5 <= e.level <= 9]
high_level_enemies = [e for e in enemies if e.level >= 10]

def get_random_enemy(player):
    """根据玩家等级选择合适的敌人"""
    if player.level <= 4:
        enemy_list = low_level_enemies
    elif 5 <= player.level <= 9:
        enemy_list = mid_level_enemies
    else:
        enemy_list = high_level_enemies

    enemy = random.choice(enemy_list)
    enemy.HP = enemy.MaxHP  # 确保满血
    enemy.MP = enemy.MaxMP
    return enemy
