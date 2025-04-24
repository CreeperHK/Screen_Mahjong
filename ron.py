from collections import Counter


def thirteen_orphans(hand_card, orphans):
    # 十三么特別判斷
    return sorted(set(hand_card)) == sorted(orphans)

def seven_pair(hand_card):
    # 七對子特別判斷
    return len(set(hand_card)) == 7

def nine_lantern(hand_card, lantern):
    # 九蓮寶燈特別判斷
    return sorted(set(hand_card)) == sorted(lantern)

def can_form_groups(tile_count):
    # 嘗試組成四個雀組
    for tile in sorted(tile_count.keys()):
        while tile_count[tile] > 0:
            # 檢查刻子
            if tile_count[tile] >= 3:
                tile_count[tile] -= 3
            # 檢查順子（只對數字牌適用）
            elif (tile + 1) in tile_count and (tile + 2) in tile_count and \
                 tile_count[tile + 1] > 0 and tile_count[tile + 2] > 0:
                tile_count[tile] -= 1
                tile_count[tile + 1] -= 1
                tile_count[tile + 2] -= 1
            else:
                break
    # 檢查是否所有牌都被使用
    return all(count == 0 for count in tile_count.values())

def can_win(tiles):
    tiles = sorted(tiles)
    changes = {10:15, 30:35, 50:55, 71:71, 72:73, 73:75, 74:77, 75:81, 76:83, 77:85}
    for i in range(len(tiles)):
        if tiles[i] in changes:
            tiles[i] = changes[tiles[i]]

    # 檢查牌數
    if len(tiles) != 14:
        #print("牌數不正確. (!=14)")
        return False

    # 檢查牌型張數
    for i in tiles:
        count = tiles.count(i)
        if count > 4:
            #print("牌數不正確. 同一種牌多於四張")
            return False

    # 計算每種牌的數量
    tile_count = Counter(tiles)

    # 十三么牌型
    thirteen_hand = thirteen_orphans(tiles, [11,19,31,39,51,59,71,73,75,77,81,83,85])
    if thirteen_hand == True:
        return True

    # 七對子牌型
    seven_hand = seven_pair(tiles)
    if seven_hand == True:
        return True
    
    # 九蓮寶燈牌型
    all_lantern = [
        [11,12,13,14,15,16,17,18,19],
        [31,32,33,34,35,36,37,38,39],
        [51,52,53,54,55,56,57,58,59]
    ]
    pairs = [(11, 19, 0), (31, 39, 1), (51, 59, 2)]
    nine_hand = False

    for a, b, idx in pairs:
        if tiles.count(a) >= 3 and tiles.count(b) >= 3:
            nine_hand = nine_lantern(tiles, all_lantern[idx])
            break
    
    if nine_hand == True:
        return True

    # 一般牌型
    for tile in list(tile_count):
        if tile_count[tile] >= 2:
            # 移除雀頭
            tile_count[tile] -= 2
            if can_form_groups(tile_count):
                return True
            # 恢復雀頭
            tile_count[tile] += 2

    return False

if __name__ in '__main__':
    # 手牌萬子 (11-19)、筒子 (31-39)、索子 (51-59)、字牌 (71,73,75,77,81,83,85)
    hand = [33,34,30,35,37,38,39,75,75,75,32,57,57,57]  

    print("手牌:", hand)
    if can_win(hand):
        print("可以和牌")
    else:
        print("不可以和牌")
