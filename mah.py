import pickle
from utils import *
from dfs import *
return_list = []

def yanhu(hc: str):
    hc = convert_hc_to_list(hc)
    if sum(hc) != 14:
        raise ValueError("请传入14位手牌.")
    with open("ron_set.pickle", "rb") as f:
        ron_set = pickle.load(f)
    ehc = encode_hand_cards(hc)
    if ehc in ron_set:
        print("RON!")
    else:
        print("nothing happens.")


def calc_shanten_13(hc=None, hc_list=None):
    if hc_list:
        hc = hc_list
    else:
        hc = convert_hc_to_list(hc)
    if sum(hc) != 13:
        raise ValueError("请传入13位手牌.")
    m = get_mianzi(hc)
    if not m:
        m = [[]]
    xt_list = [[],[],[],[],[],[],[],[],]
    for x in m:
        mianzi_count = len(x)
        thc = get_trimed_hc(hc.copy(), x)
        dazi_list = get_dazi(thc)
        da_list_xt_min = 999
        for dazi in dazi_list:
            # check AA
            if_quetou = 0
            for y in dazi:
                if y[1] > 0:
                    if_quetou = 1
            dazi_count = len(dazi)
            xt = calc_xiangting(mianzi_count, dazi_count, if_quetou)
            if xt <= da_list_xt_min:
                tthc = get_trimed_dazi(thc.copy(), dazi)
                guzhang_list = get_guzhang(tthc)
                tenpai = get_tenpai_from_dazi(dazi, xt)

                # distance = 0
                if xt == 0:
                    if not dazi:
                        tenpai += guzhang_list
                # if distance = 1
                if xt == 1:
                    if dazi_count == 1:
                        if if_quetou:
                            ga = get_guzhang_around(guzhang_list)
                            tenpai += ga
                            tenpai += guzhang_list
                        else:
                            tenpai += guzhang_list
                    if dazi_count == 2:
                        for d in dazi:
                            i = d[0]
                            if d[1] > 0:
                                tenpai.append(i)
                            elif d[2] > 0:
                                tenpai.append(i)
                                tenpai.append(i + 1)
                            elif d[3] > 0:
                                tenpai.append(i)
                                tenpai.append(i + 2)
                # distance >= 2
                if xt >= 2:
                    if mianzi_count + dazi_count < 5:
                        if mianzi_count + dazi_count == 4 and not if_quetou:
                            less_than5 = get_md_less_than5(tthc,0)
                            tenpai += less_than5
                        else:
                            less_than5 = get_md_less_than5(tthc)
                            tenpai += less_than5
                        #pass
                    elif mianzi_count + dazi_count >=5:
                        if not if_quetou:
                            for d in dazi:
                                i = d[0]
                                if d[1] > 0:
                                    tenpai.append(i)
                                elif d[2] > 0:
                                    tenpai.append(i)
                                    tenpai.append(i + 1)
                                elif d[3] > 0:
                                    tenpai.append(i)
                                    tenpai.append(i + 2)
                            tenpai += guzhang_list
                tenpai = list(set(tenpai))
                tenpai.sort()
                xt_list[xt] += tenpai
    for y in range(len(xt_list)):
        if xt_list[y]:
            return (y, list(set(xt_list[y])))


# 一般形牌理分析
def calc_shanten_14(hc: str):
    hc = convert_hc_to_list(hc)
    if sum(hc) != 14:
        raise ValueError("请传入14位手牌.")
    xt_list = []
    for x in range(len(hc)):
        if hc[x] > 0:
            # 变位
            hc[x] -= 1
            xt = calc_shanten_13(hc_list=hc)
            if xt:
                xt_list.append([x, xt])
            # 复位
            hc[x] += 1
    # 最小向听数
    xt_min = min([x[1][0] for x in xt_list])
    if xt_min == 0:
        return_list = ["聽牌"]
    else:
        return_list = [f'{xt_min}向聽']
        
    card_advice_list = []

    for xxt in xt_list:
        xt = xxt[1]
        if xt[0] == xt_min:
            xt[1].sort()
            msum = calc_tenpai_sum(hc, xt[1])
            card_advice_list.append([xxt[0], xt[1], msum])
    card_advice_list.sort(key=lambda x: x[2], reverse=1)
    for x in card_advice_list:
        a = convert_num_to_card(x[0])
        b = [convert_num_to_card(x) for x in x[1]]
        c = x[2]
        return_str = [a, b, c]
        return_list.append(return_str)
    
    return return_list
