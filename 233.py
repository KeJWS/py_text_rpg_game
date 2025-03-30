# 修改战斗的处理部分

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

def get_random_enemy():
    # 修改敌人生成，确保其血量合理，不会过低
    enemy = random.choice(enemies)
    enemy.HP = enemy.MaxHP  # 确保每次战斗开始时敌人的血量是满的
    enemy.MP = enemy.MaxMP  # 同时恢复敌人的魔法值
    return enemy

# 战斗逻辑处理
def battle(player):
    enemy = get_random_enemy()  # 获取一个随机敌人
    battle_instance = Battle(player, enemy)
    battle_instance.process_battle()
