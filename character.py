import random

class Character:
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill):
        self.name = name
        self.MaxHP = max_hp
        self.MaxMP = max_mp
        self.HP = max_hp
        self.MP = max_mp
        self.ATK = atk
        self.DEF = defense
        self.MAT = mat
        self.MDF = mdf
        self.AGI = agi
        self.LUK = luk
        self.skill = skill
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50
        self.gold = 0

    def calculate_damage(self, opponent, is_magical=False):
        stat_attack = self.MAT if is_magical else self.ATK
        stat_defense = opponent.MDF if is_magical else opponent.DEF
        base_damage = max(1, stat_attack * 4 - stat_defense * 2)
        return self.apply_critical_hit(base_damage)
    
    def apply_critical_hit(self, damage):
        if random.randint(1, 100) <= self.LUK / 2:
            crit_multiplier = random.choice([1.5, 2])
            print(f"{self.name} 造成暴击！伤害 x{crit_multiplier}")
            return int(damage * crit_multiplier)
        return damage

    def attack(self, opponent):
        damage = self.calculate_damage(opponent)
        opponent.HP -= damage
        print(f"{self.name} 攻击 {opponent.name}，造成 {damage} 伤害！")

    def use_skill(self, opponent):
        if self.MP >= 10:
            self.MP -= 10
            damage = self.calculate_damage(opponent, is_magical=True)
            opponent.HP -= damage
            print(f"{self.name} 使用 {self.skill}，造成 {damage} 伤害！ (MP -10)")
        else:
            print("MP不足，无法使用技能！")
            return False
        return True

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} 获得 {amount} 经验值！")
        if self.exp >= self.exp_to_next:
            self.level_up()

    def gain_gold(self, amount):
        self.gold += amount
        print(f"{self.name} 获得 {amount} 金币！(当前金币: {self.gold})")

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.5)
        stats = ["MaxHP", "MaxMP", "ATK", "DEF", "MAT", "MDF", "AGI", "LUK"]
        increments = [20, 10, 3, 2, 3, 2, 1, 1]
        for stat, inc in zip(stats, increments):
            setattr(self, stat, getattr(self, stat) + inc)
        self.HP, self.MP = self.MaxHP, self.MaxMP
        print(f"{self.name} 升级到 {self.level} 级！")
        print(f"{self.name}: (MaxHP: {self.MaxHP}, MaxMP: {self.MaxMP}, ATK: {self.ATK}, DEF: {self.DEF}, MAT: {self.MAT}, MDF: {self.MDF}, AGI: {self.AGI}, LUK: {self.LUK}, 技能: {self.skill})")

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill, exp_reward, gold_reward):
        super().__init__(name, max_hp, max_mp, atk, defense, mat, mdf, agi, luk, skill)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward