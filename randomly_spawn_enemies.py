import random

# 怪物名和技能池
names = [
    "哥布林", "狼", "骷髅战士", "秃鹫", "巨魔", "黑龙", "死亡法师", "无头骑士",
    "史莱姆", "盗贼", "石像鬼", "巫妖", "火元素", "冰霜巨人", "暗影猎手"
]

skills = [
    "挥砍", "撕咬", "重击", "狂暴挥砍", "暗影烈焰", "死亡射线", "超神斩", "火球", "寒冰箭", "毒液喷吐"
]

# 前缀及其倍率
prefixes = {
    "虚弱的": 0.7,
    "普通的": 1.0,
    "强壮的": 1.2,
    "精英的": 1.5,
    "超神的": 2.0
}

def generate_level_range():
    start = random.randint(1, 95)
    end = random.randint(start + 1, min(start + 5, 100))
    return start, end

def scale_stat(base, avg_level, prefix_multiplier, max_level=20):
    scale = avg_level / max_level
    stat = base[0] + (base[1] - base[0]) * scale
    return int(stat * prefix_multiplier)

def generate_enemy(id):
    # 前缀与倍率
    prefix, multiplier = random.choice(list(prefixes.items()))
    name = prefix + random.choice(names)
    
    min_lv, max_lv = generate_level_range()
    avg_lv = (min_lv + max_lv) / 2
    
    max_hp = scale_stat((80, 1000), avg_lv, multiplier)
    max_mp = scale_stat((10, 300), avg_lv, multiplier)
    atk = scale_stat((10, 100), avg_lv, multiplier)
    defense = scale_stat((5, 60), avg_lv, multiplier)
    mat = scale_stat((5, 120), avg_lv, multiplier)
    mdf = scale_stat((5, 100), avg_lv, multiplier)
    agi = scale_stat((5, 50), avg_lv, multiplier)
    luk = scale_stat((3, 30), avg_lv, multiplier)
    
    skill = random.choice(skills)
    exp_reward = scale_stat((20, 1000), avg_lv, multiplier)
    gold_reward = scale_stat((10, 500), avg_lv, multiplier)
    level_range = f"{min_lv}-{max_lv}"
    
    return f"{id},{name},{max_hp},{max_mp},{atk},{defense},{mat},{mdf},{agi},{luk},{skill},{exp_reward},{gold_reward},{level_range}"

def generate_enemy_list(count=10):
    lines = ["id,name,max_hp,max_mp,atk,defense,mat,mdf,agi,luk,skill,exp_reward,gold_reward,level_range"]
    for i in range(1, count + 1):
        lines.append(generate_enemy(i))
    return "\n".join(lines)

# 示例运行
enemy_csv = generate_enemy_list(99)
print(enemy_csv)
