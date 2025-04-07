import random
from test.clear_screen import enter_clear_screen

class Inventory:
    def __init__(self):
        self.items = []

class Character:
    def __init__(self, name, description, base_stats) -> None:
        self.name = name
        self.base_stats = {
            "max_hp": 200, 
            "max_mp": 50, 
            "atk": 10, 
            "def": 10,
            "mat": 5, 
            "mdf": 10, 
            "agi": 10, 
            "luk": 10,
            "crit": 0
        }
        self.stats = self.base_stats.copy()
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["mp"] = self.stats["max_mp"]

        self.base_aptitudes = {
            "str": 0,
            "dex": 0,
            "int": 0,
            "wis": 0,
            "const": 0
        }
        self.aptitudes = self.base_aptitudes.copy()
        self.aptitude_points = 0

        self.skills = []
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50 
        self.gold = 0
        self.equipment = {
            "weapon": None,
            "armor": None
        }
        self.inventory = Inventory()

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} 获得 {amount} 经验值! ")
        while self.exp >= self.exp_to_next:
            self.level_up()

    def gain_gold(self, amount):
        self.gold += amount
        print(f"{self.name} 获得 {amount} 金币! (\033[33m💰: {self.gold}\033[0m)")

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(50 * (self.level ** 1.5))
        growth = {
            "max_hp": 50,
            "max_mp": 10,
            "atk": 2,
            "def": 2,
            "mat": 1,
            "mdf": 2,
            "agi": 1,
            "luk": 1
        }
        for stat, inc in growth.items():
            self.stats[stat] += inc
        self.aptitude_points += 1
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["mp"] = self.stats["max_mp"]
        print(f"\033[33m{self.name} 升级到 {self.level} 级!\033[0m")

    def show_stats(self):
        stats_template = (
            f"----------------------------------\n"
            f"  STATS               💰: {self.gold}\n"
            f"----------------------------------\n"
            f"      LV: {self.level}        EXP: {self.exp}/{self.exp_to_next}\n"
            f"      \033[31mHP: {self.stats['hp']}/{self.stats['max_hp']}\033[0m    \033[34mMP: {self.stats['mp']}/{self.stats['max_mp']}\033[0m\n"
            f"      ATK: {self.stats['atk']}        DEF: {self.stats['def']}\n"
            f"      MAT: {self.stats['mat']}        MDF: {self.stats['mdf']}\n"
            f"      AGI: {self.stats['agi']}        CRT: {self.stats['crit']}\n"
            f"----------------------------------\n"
            f"  APTITUDES\n"
            f"----------------------------------\n"
            f"      STR: {self.aptitudes['str']}        DEX: {self.aptitudes['dex']}\n"
            f"      INT: {self.aptitudes['int']}        WIS: {self.aptitudes['wis']}\n"
            f"      CONST: {self.aptitudes['const']}\n"
            f"----------------------------------\n"
            f"  EQUIPMENT\n"
            f"----------------------------------"
        )
        print(stats_template)
        for slot, item in self.equipment.items():
            print(f"    {slot}: {item.name if item else '无'}")
        enter_clear_screen()

    def assign_aptitude_points(self):
        # TODO: 实现手动分配点数系统，例如升级获得点数后玩家自行分配
        return

    def update_stats_to_aptitudes(self, aptitude):
        # TODO: 基于aptitude修改stats，例如STR影响ATK，CONST影响HP等
        return

    def reset_stats(self):
        self.level = 1 
        self.exp = 0
        self.exp_to_next = 50
        self.stats = self.base_stats.copy()
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["mp"] = self.stats["max_mp"]
        self.aptitudes = self.base_aptitudes.copy()
        print(f"{self.name} 的状态已重置。")
