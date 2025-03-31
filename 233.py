def drop(self, item_list):
    """根据掉落概率随机掉落物品"""
    dropped_items = []
    
    if not self.drop_items:
        print(f"{self.name} 没有掉落任何物品。")
        return dropped_items

    for item_id, drop_chance in self.drop_items.items():
        if random.random() <= drop_chance:  # 确保 drop_chance 是 0.0 ~ 1.0
            item = item_list.get(item_id)
            if item:
                dropped_items.append(item)
            else:
                print(f"⚠️ 警告：未找到 ID 为 {item_id} 的物品。")
    
    if not dropped_items:
        print(f"{self.name} 没有掉落物品。")
    
    return dropped_items
