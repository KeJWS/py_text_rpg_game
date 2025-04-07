import character_copy
from unittest.mock import patch

with patch("test.clear_screen.enter_clear_screen", lambda: None):

    print("=== 创建角色 ===")
    hero = character_copy.Character("Rik", "", "")

    print("\n=== 显示初始状态 ===")
    hero.show_stats()

    print("\n=== 获得经验 (999) 触发升级 ===")
    hero.gain_exp(999)

    print("\n=== 获得金币 (999) ===")
    hero.gain_gold(999)

    print("\n=== 再次显示状态（查看升级变化） ===")
    hero.show_stats()

    print("\n=== 重置状态 ===")
    hero.reset_stats()

    print("\n=== 重置后状态展示 ===")
    hero.show_stats()
