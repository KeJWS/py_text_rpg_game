def rebirth(player):
    """执行转生逻辑，保留物品、武器、防具、金币，重置角色状态"""
    print("\n💀 你已死亡！但你可以选择转生继续冒险！")
    choice = input("是否转生？(y/n): ").lower()
    
    if choice == "y":
        print("✨ 你获得了新生！但属性被重置...")
        player.level = 1
        player.exp = 0
        player.exp_to_next = 100  # 假设初始升级经验为100
        player.MaxHP = player.base_MaxHP  # 恢复初始HP
        player.MaxMP = player.base_MaxMP  # 恢复初始MP
        player.ATK = player.base_ATK
        player.DEF = player.base_DEF
        player.MAT = player.base_MAT
        player.MDF = player.base_MDF
        player.AGI = player.base_AGI
        player.LUK = player.base_LUK
        player.HP = player.MaxHP  # 满血复活
        player.MP = player.MaxMP  # 满魔复活
        
        print("🎒 你的物品、装备和金币都被保留了！")
        input("\n按 Enter 继续冒险...")
    else:
        print("👋 游戏结束，再见！")
        exit()
