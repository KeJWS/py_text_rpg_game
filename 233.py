class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combatants = [player, enemy]
        self.status_effects = {player.name: {}, enemy.name: {}}
        self.turn_order = self.get_battle_order()
        self.turn_count = 1  # 新增回合计数

    def process_battle(self):
        print(f"\n⚔️ 你遇到了 {self.enemy.name}！⚔️")
        while self.player.HP > 0 and self.enemy.HP > 0:
            print(f"\n==== 🌀 第 {self.turn_count} 回合 ====")
            print(f"💖 你的生命值: {self.player.HP}/{self.player.MaxHP} | MP: {self.player.MP}/{self.player.MaxMP}")
            print(f"💀 {self.enemy.name} 的生命值: {self.enemy.HP}/{self.enemy.MaxHP} | MP: {self.enemy.MP}/{self.enemy.MaxMP}")
            print("🔄 行动顺序:", " -> ".join([c.name for c in self.turn_order]))

            for combatant in self.turn_order:
                if combatant.HP <= 0:
                    continue
                if not self.apply_status_effects(combatant):
                    continue  # 若被眩晕，跳过回合

                if combatant == self.player:
                    if self.player_action():
                        return  # 逃跑成功，结束战斗
                else:
                    self.enemy_action(combatant)

            # 清除单回合状态
            for combatant in self.combatants:
                self.status_effects[combatant.name].pop('defend', None)

            self.turn_count += 1  # 进入下一回合

        self.battle_result()

    def player_action(self):
        action = input("选择行动 (a. 攻击 s. 使用技能 q. 逃跑 d. 防御): ")
        if action == "a":
            damage = self.player.attack(self.enemy)
            print(f"🗡️ 你攻击了 {self.enemy.name}，造成 {damage} 伤害！")
        elif action == "s":
            skill_used, skill_name, mp_cost = self.player.use_skill(self.enemy)
            if skill_used:
                print(f"✨ 你使用了技能 '{skill_name}'，消耗 {mp_cost} MP！")
            else:
                print("❌ 技能释放失败（可能是MP不足）！")
                return False  # 取消行动
        elif action == "q":
            if self.try_escape():
                return True  # 逃跑成功
        elif action == "d":
            self.status_effects[self.player.name]['defend'] = True
            print("🛡️ 你进入防御状态，本回合受到的伤害减少 50%！")
        else:
            print("⚠️ 无效的选择，默认进行普通攻击！")
            damage = self.player.attack(self.enemy)
            print(f"🗡️ 你攻击了 {self.enemy.name}，造成 {damage} 伤害！")
        return False

    def enemy_action(self, enemy):
        """敌人行为逻辑"""
        if enemy.HP < enemy.MaxHP * 0.3 and random.random() < 0.3:
            print(f"⚠️ {enemy.name} 进入防御状态！")
            self.status_effects[enemy.name]['defend'] = True
            return
        
        damage = enemy.calculate_damage(self.player)
        if 'defend' in self.status_effects[self.player.name]:
            damage //= 2  # 玩家防御时伤害减少50%
            print(f"🛡️ 你成功防御，伤害减少为 {damage}！")
        else:
            print(f"🔥 {enemy.name} 攻击了你，造成 {damage} 伤害！")
        self.player.HP -= damage

    def try_escape(self):
        escape_chance = min(90, max(10, self.player.AGI * 3))  # 逃跑概率：10% - 90%
        if random.randint(1, 100) <= escape_chance:
            print("🏃 你成功逃跑了！")
            return True
        else:
            print(f"🚫 {self.enemy.name} 阻止了你的逃跑！")
            return False
