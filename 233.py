from character import Weapon, Equipment  # 确保在函数内部导入以避免循环引用
from game_data import load_weapon_by_id, load_armor_by_id  # 用于从ID加载数据

@staticmethod
def load_character(character):
    """从JSON文件加载角色数据"""
    if not os.path.exists(SaveManager.SAVE_FILE):
        print("⚠️ 没有找到存档文件！")
        return False

    with open(SaveManager.SAVE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

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

    # ⚠️ 重新创建 `Weapon` 和 `Equipment` 实例
    character.weapons = {id: Weapon(**info) for id, info in data["weapons"].items()}
    character.armors = {id: Equipment(**info) for id, info in data["armors"].items()}

    # ⚠️ 重新加载装备
    character.weapon = character.weapons.get(data["weapon"], None)  # 从字典获取武器
    character.equipment = character.armors.get(data["equipment"], None)  # 从字典获取护甲

    print("✅ 存档加载成功！")
    return True
