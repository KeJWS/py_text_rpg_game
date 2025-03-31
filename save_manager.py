import json
import os

class SaveManager:
    SAVE_FILE = "save.json"

    @staticmethod
    def save_character(character):
        """将角色数据保存到JSON文件"""
        data = {
            "name": character.name,
            "level": character.level,
            "exp": character.exp,
            "exp_to_next": character.exp_to_next,
            "gold": character.gold,
            "HP": character.HP,
            "MP": character.MP,
            "MaxHP": character.MaxHP,
            "MaxMP": character.MaxMP,
            "ATK": character.ATK,
            "DEF": character.DEF,
            "MAT": character.MAT,
            "MDF": character.MDF,
            "AGI": character.AGI,
            "LUK": character.LUK,
            "weapon": character.weapon.id if character.weapon else None,
            "equipment": character.equipment.id if character.equipment else None,
            "weapons": {id: vars(weapon) for id, weapon in character.weapons.items()},
            "armors": {id: vars(armor) for id, armor in character.armors.items()},
            "inventory": character.inventory.items  # 假设 inventory.items 是字典
        }

        with open(SaveManager.SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("💾 存档已保存！")

    @staticmethod
    def load_character(character):
        """从JSON文件加载角色数据"""
        if not os.path.exists(SaveManager.SAVE_FILE):
            print("⚠️ 没有找到存档文件！")
            return False

        # from character import Weapon, Equipment  # ⬅ **改成在函数内部导入**

        with open(SaveManager.SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # 这里才导入 game_data，避免循环依赖
        from game_data import load_weapon_by_id, load_armor_by_id

        character.name = data["name"]
        character.level = data["level"]
        character.exp = data["exp"]
        character.exp_to_next = data["exp_to_next"]
        character.gold = data["gold"]
        character.HP = data["HP"]
        character.MP = data["MP"]
        character.MaxHP = data["MaxHP"]
        character.MaxMP = data["MaxMP"]
        character.ATK = data["ATK"]
        character.DEF = data["DEF"]
        character.MAT = data["MAT"]
        character.MDF = data["MDF"]
        character.AGI = data["AGI"]
        character.LUK = data["LUK"]

         # 读取武器和防具
        character.weapon = load_weapon_by_id(data["weapon"]) if data["weapon"] else None
        character.equipment = load_armor_by_id(data["equipment"]) if data["equipment"] else None

        # 读取武器库
        # character.weapons = {weapon_id: load_weapon_by_id(weapon_id) for weapon_id in data.get("weapons", [])}

        # 读取护甲库
        # character.armors = {armor_id: load_armor_by_id(armor_id) for armor_id in data.get("armors", [])}

        # character.inventory.items = data["inventory"]

        print("✅ 存档加载成功！")
        return True
