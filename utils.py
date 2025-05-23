import re, math

# form ABC
def compose_gen_sz(sz) -> list:
    mycompose = []

    def myrecursion(fr=None, br=None):
        if fr is not None and br is not None:
            mycompose.append([sz - fr, br, fr - br])
            return
        else:
            for k in range(0, fr + 1):
                myrecursion(fr, k)

    for x in range(sz + 1):
        fr = sz - x
        myrecursion(x)
    return mycompose


# form AAA 
def compose_gen_kz(kz) -> list:
    mycompose = []

    def myrecursion(fr=None, br=None, cr=None):
        if fr is not None and br is not None and cr is not None:
            mycompose.append([kz - fr, br, cr, fr - br - cr])
            return
        elif fr is not None and br is not None:
            for k in range(0, fr - br + 1):
                myrecursion(fr, br, k)
        else:
            for k in range(0, fr + 1):
                myrecursion(fr, k)

    for x in range(kz + 1):
        fr = kz - x
        myrecursion(x)
    return mycompose


# AAA style generate (for Z only)
def produce_kz_zipai(index) -> list:
    mykz = [0] * 7
    mykz[index] += 3
    return mykz


# AAA style generate
def produce_kz(index) -> list:
    mykz = [0] * 9
    mykz[index] += 3
    return mykz


# ABC style generate
def produce_sz(index) -> list:
    mysz = [0] * 9
    mysz[index] += 1
    mysz[index + 1] += 1
    mysz[index + 2] += 1
    return mysz


# encode hand tiles
def encode_hand_cards(hc: list) -> str:
    def encode_hc(ehc, zipai=False):
        if zipai:
            mhc = "0".join(str(y) for y in ehc)
        else:
            mhc = "".join(str(y) for y in ehc)
        mhc = mhc.strip("0")
        mhc = re.sub(r"0{2,}", "0", mhc)
        return mhc

    hc_wan = hc[0:9]
    hc_tiao = hc[9:18]
    hc_tong = hc[18:27]
    hc_zi = hc[27:34]

    ehc_to_join = []
    for x in [
        encode_hc(hc_wan),
        encode_hc(hc_tiao),
        encode_hc(hc_tong),
        encode_hc(hc_zi, zipai=True),
    ]:
        if x:
            ehc_to_join.append(x)
    return "0".join(ehc_to_join)


# convert hand tiles into list
def convert_hc_to_list(hc: str) -> list:
    if not hc:
        raise ValueError
    # 0 -> 5
    hc = hc.replace("0", "5")
    hc_list = [0] * 34
    pattern = re.compile(r"\d+[mspz]")
    result = pattern.findall(hc)
    for x in result:
        if x[-1] == "m":
            for y in x[:-1]:
                hc_list[int(y) - 1] += 1
        if x[-1] == "s":
            for y in x[:-1]:
                hc_list[int(y) - 1 + 9] += 1
        if x[-1] == "p":
            for y in x[:-1]:
                hc_list[int(y) - 1 + 18] += 1
        if x[-1] == "z":
            for y in x[:-1]:
                hc_list[int(y) - 1 + 27] += 1
    return hc_list


# encode for return
def encode_arbitrary_cards(hc: list):
    def encode_hc(ehc, if_zi=False):
        if if_zi:
            mhc = "0".join(str(y) for y in ehc)
        else:
            mhc = "".join(str(y) for y in ehc)
        mhc = mhc.strip("0")
        mhc = re.sub(r"0{2,}", "0", mhc)

        return mhc

    return encode_hc(hc)


# convert into different style
def convert_num_to_card(num: int):
    mcard = None
    if num < 9:
        mcard = str(num + 1) + "m"
    elif 9 <= num < 18:
        mcard = str(num - 9 + 1) + "s"
    elif 18 <= num < 27:
        mcard = str(num - 18 + 1) + "p"
    else:
        mcard = ["1z", "2z", "3z", "4z", "5z", "6z", "7z"][num - 27]
    return mcard


# tiles -AA for cal
def get_trimed_hc(hc, mianzi):
    for x in mianzi:
        i = x[0]
        if x[1] > 0:
            hc[i] -= 1
            hc[i + 1] -= 1
            hc[i + 2] -= 1
        elif x[2] > 0:
            hc[i] -= 3
    return hc


# tiles - all Z
def get_trimed_dazi(hc, dazi):
    for x in dazi:
        i = x[0]
        if x[1] > 0:
            hc[i] -= 2
        elif x[2] > 0:
            hc[i] -= 1
            hc[i + 1] -= 1
        elif x[3] > 0:
            hc[i] -= 1
            hc[i + 2] -= 1
    return hc


# 258 get
def get_guzhang(hc):
    guzhang_list = []
    for x in range(len(hc)):
        if hc[x] == 1:
            guzhang_list.append(x)
    return guzhang_list


# get usful tile in 258
def get_guzhang_around(guzhang_list: list):
    g = []
    for x in guzhang_list:
        if x < 27:
            for y in [x - 2, x - 1, x + 1, x + 2]:
                if y >= 0 and math.floor(y / 9) == math.floor(x / 9):
                    g.append(y)
    return g


# distance calculation
def get_md_less_than5(hc, new_dazi = 1):
    guzhang_list = []
    for x in range(len(hc)):
        if hc[x] == 1:
            guzhang_list.append(x)
            if x < 27 and new_dazi:
                for y in [x - 2, x - 1, x + 1, x + 2]:
                    if y >= 0 and math.floor(y / 9) == math.floor(x / 9):
                        guzhang_list.append(y)
    return guzhang_list


# suggest calculation
def get_tenpai_from_dazi(dazi, xt):
    # dazi = [(2, 1, 0, 0), (18, 0, 0, 1)]
    tenpai = []
    # distance >= 1.0
    if xt == 0:
        if len(dazi) == 2:
            if dazi[0][1] > 0 and dazi[1][1] > 0:
                tenpai.append(dazi[0][0])
                tenpai.append(dazi[1][0])
            else:
                for x in dazi:
                    index = x[0]
                    # [11]
                    if x[2] > 0:
                        if index in [0, 9, 18]:
                            tenpai.append(index + 2)
                        elif index in [7, 16, 25]:
                            tenpai.append(index - 1)
                        else:
                            tenpai.append(index - 1)
                            tenpai.append(index + 2)
                    # [101]
                    if x[3] > 0:
                        tenpai.append(index + 1)
        return tenpai
    # distance <= 2.0
    for x in dazi:
        index = x[0]
        # [2]
        if x[1] > 0:
            tenpai.append(x[0])
        # [11]
        if x[2] > 0:
            if index in [0, 9, 18]:
                tenpai.append(index + 2)
            elif index in [7, 16, 25]:
                tenpai.append(index - 1)
            else:
                tenpai.append(index - 1)
                tenpai.append(index + 2)
        # [101]
        if x[3] > 0:
            tenpai.append(index + 1)
    return tenpai


# distance calculation
def calc_xiangting(m, d, if_quetou):
    if m + d <= 5:
        c = 0
    else:
        c = m + d - 5
    if m + d <= 4:
        q = 1
    else:
        if if_quetou:
            q = 1
        else:
            q = 0
    x = 9 - 2 * m - d + c - q
    return x


# count calculation
def calc_tenpai_sum(hc: list, tenpai: list):
    msum = 0
    for x in tenpai:
        msum += 4 - hc[x]
    return msum
